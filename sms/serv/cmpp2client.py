# -*- coding: utf-8 -*-

import hashlib
import Queue
import time

from X.tools.task import sleep, gevent_task, keep_interval, delay_exec
from X.tools.exception import sms_exception
from X.tools.log import log
from sms.serv.socketlib import SocketClient, SSLClient
from sms.serv.cmpp2frame import *
from sms.serv.cmpp2handler import Cmpp2Handler
import sms.serv.smstools


# 1、重连之后清空slide window 2、设置手动重启功能

class Cmpp2Client:
    # default_charset='gbk'
    # default_charset='UTF-16BE'

    def __init__(self, config):
        self.config = config
        # 默认参数设定
        self.fetch_size = self.config.cmpp_commit_speed  # 每次数据库中读取待发短信量
        self.buffer_size = 10  # 短信提交队列大小
        self.wait_size = 1024
        self.bulk_size = 100  # 待发短信批量入库块大小
        self.fetch_interval = 1

        self.handler = Cmpp2Handler()

        self.task_queue = sms.serv.smstools.SendTaskQueue()

        self.send_once_interval = 1.0 / self.config.cmpp_commit_speed

        self.reconnect = True
        self.reconnect_interval = 1

        self.commit_queue = Queue.Queue()
        self.commit_resp_wait_list = {}

        self.frm_seq = sms.serv.smstools.MessageSquence(bit=32)
        self.msg_seq = sms.serv.smstools.MessageSquence(bit=7)

        self.send_queue = Queue.Queue()

        self.frame_handler = Cmpp2FrameHandler()
        ssl_mode = self.config.cmpp_ssl
        source = (self.config.sock_source_ip.encode(), self.config.sock_source_port)
        target = (self.config.sock_target_ip.encode(), self.config.sock_target_port)
        if ssl_mode == 'enabled':
            self.socket_client = SSLClient(source, target, self.frame_handler)
        else:
            self.socket_client = SocketClient(source, target, self.frame_handler)

        self.cmpp_status = -1

    @gevent_task
    @sms_exception
    def start_serv(self):
        while self.reconnect:
            self.reset_environment()
            self.auto_connect()
            self.start_send_daemon()
            self.recv_daemon()
            log(
                title='CMPP2_SERV_CONTINUE_%s_%s_RECONNECT=%s' % (
                    self.config.cmpp_sp_id.encode(), self.config.cmpp_src_id.encode(), self.reconnect),
                content=None,
                logger='sms',
                level='error'
            )

    def stop_serv(self, sleep_time=1.0):
        self.reconnect = False
        self.cmpp_terminate()
        sleep(sleep_time / 5)
        sleep(sleep_time / 5)
        sleep(sleep_time / 5)
        sleep(sleep_time / 5)
        sleep(sleep_time / 5)
        self.socket_client.close()
        log(
            title='CMPP2_STOP_SERV_%s_%s' % (self.config.cmpp_sp_id.encode(), self.config.cmpp_src_id.encode()),
            content=None,
            logger='sms',
            level='error'
        )

    def auto_connect(self):
        status = -1
        while self.reconnect and status != 0:
            try:
                self.socket_client.connect()
                status = self.cmpp_connect()
            except:
                log(
                    title='CMPP2_AUTO_CONNECT_%s_%s' % (
                        self.config.cmpp_sp_id.encode(), self.config.cmpp_src_id.encode()),
                    content=None,
                    logger='sms',
                    level='error'
                )
            sleep(self.reconnect_interval)
        self.cmpp_status = status
        return status

    def recv_daemon(self):
        try:
            while True:
                self.recv_once()
        except:
            # import traceback
            # traceback.print_exc()
            pass
        finally:
            self.socket_client.close()
            log(
                title='CMPP2_SOCK_RECV_STOP_%s_%s' % (
                    self.config.cmpp_sp_id.encode(), self.config.cmpp_src_id.encode()),
                content=None,
                logger='sms',
                level='error'
            )

    def recv_once(self):
        frame = self.socket_client.recv()
        ID = frame.ID
        log(
            title='CMPP2_RECEIVE_FRAME_%s_%s_%s' % (
                self.config.cmpp_sp_id.encode(), self.config.cmpp_src_id.encode(),
                Cmpp2FrameHandler.ID_TO_NAME[frame.ID]),
            content=frame.ID == 0x00000005 and [frame.__dict__, frame.status_report.__dict__] or frame.__dict__,
            logger='sms',
            level='debug'
        )

        if ID == CMPP2_TERMINATE.ID:
            terminate = frame
            terminate_resp = CMPP2_TERMINATE_RESP()
            self.send_queue_put(terminate_resp, terminate)
        elif ID == CMPP2_DELIVER.ID:
            deliver = frame
            deliver_resp = self.recv_sms(frame)
            self.send_queue_put(deliver_resp, deliver)
        elif ID == CMPP2_ACTIVE_TEST:
            active_test = frame
            active_test_resp = CMPP2_ACTIVE_TEST_RESP()
            active_test_resp.reserve = 0
            self.send_queue_put(active_test_resp, active_test)

        elif ID == CMPP2_TERMINATE_RESP.ID:
            self.socket_client.close()
            raise Cmpp2TerminateException('TERMINATE')
        elif ID == CMPP2_SUBMIT_RESP.ID:
            cmpp_submit_resp = CMPP2_SUBMIT_RESP
            cmpp_submit_resp = frame
            sequence_Id = cmpp_submit_resp.sequence_Id
            msg = self.commit_resp_wait_list_get(sequence_Id)
            if msg:
                if cmpp_submit_resp.result == 8:
                    self.commit_queue.put((msg.get('sms_obj'), True))
                else:
                    msg['msg_id'] = cmpp_submit_resp.msg_id
                    msg['result'] = cmpp_submit_resp.result
                    self.handler.sms_ack(self, msg)
            else:
                log(
                    title='CMPP2_SUBMIT_RESP_MATCH_NO_SEQID_%s_%s' % (
                        self.config.cmpp_sp_id.encode(), self.config.cmpp_src_id.encode()),
                    content=frame.ID == 0x00000005 and [frame.__dict__, frame.status_report.__dict__] or frame.__dict__,
                    logger='sms',
                    level='debug'
                )

        elif ID in (
                CMPP2_CONNECT.ID,
                CMPP2_CONNECT_RESP.ID,
                CMPP2_SUBMIT.ID,
                CMPP2_DELIVER_RESP.ID,
                CMPP2_QUERY.ID,
                CMPP2_QUERY_RESP.ID,
                CMPP2_CANCEL.ID,
                CMPP2_CANCEL_RESP.ID,
                CMPP2_ACTIVE_TEST_RESP.ID
        ):
            pass
        else:
            raise Cmpp2UnknownCommandIDException("bad id = 0x%08x" % ID)
        return frame

    def recv_sms(self, frame):
        # deliver=CMPP2_DELIVER
        deliver = frame
        if deliver.registered_delivery:
            status_report = deliver.status_report

            msg = {
                'dest_id': deliver.dest_id.strip(),
                'msg_content': deliver.msg_content,
                'registered_delivery': deliver.registered_delivery,
                'src_id': deliver.src_terminal_id.strip(),
                'msg_fmt': deliver.msg_fmt,
                'tp_udhi': deliver.tp_udhi,
                'msg_id': status_report.msg_id,
                'stat': status_report.stat,
                'submit_time': status_report.submit_time,
                'done_time': status_report.done_time,
                'dest_terminal_id': status_report.dest_terminal_id,
            }
            self.handler.sms_feed(self, msg)

        else:
            msg = {
                'msg_id': deliver.msg_id,
                'dest_id': deliver.dest_id,
                'service_id': deliver.service_id,
                'tp_pid': deliver.tp_pid,
                'tp_udhi': deliver.tp_udhi,
                'msg_fmt': deliver.msg_fmt,
                'src_terminal_id': deliver.src_terminal_id,
                'registered_delivery': deliver.registered_delivery,
                'msg_length': deliver.msg_length,
                'msg_content': deliver.msg_content,
                'reserved': deliver.reserved
            }
            self.handler.sms_recv(self, msg)
        deliver_resp = CMPP2_DELIVER_RESP()
        deliver_resp.msg_id = deliver.msg_id
        deliver_resp.result = 0
        return deliver_resp

    @gevent_task
    def start_send_daemon(self):
        self.send_daemon()

    def send_daemon(self):
        sock = self.socket_client.sock
        try:
            while True:
                if sock != self.socket_client.sock:
                    break
                if self.cmpp_status not in (0, 0.5):
                    break
                self.send_once()
        except:
            self.socket_client.close()
        finally:
            log(
                title='CMPP2_SOCK_SEND_STOP_%s_%s' % (
                    self.config.cmpp_sp_id.encode(), self.config.cmpp_src_id.encode()),
                content=None,
                logger='sms',
                level='error'
            )

    send_once_sleep_mode = True

    @keep_interval
    def send_once(self):
        if self.send_queue.qsize() <= 0:
            self.submit_one_sms()
        if self.send_queue.qsize() <= 0:
            self.cmpp_active_test()
            return None
        frame = self.send_queue.get()
        log(
            title='CMPP2_SEND_FRAME_%s_%s_%s' % (
                self.config.cmpp_sp_id.encode(), self.config.cmpp_src_id.encode(),
                Cmpp2FrameHandler.ID_TO_NAME[frame.ID]),
            content=frame.__dict__,
            logger='sms',
            level='debug'
        )
        self.socket_client.send(frame)
        return frame

    def send_queue_put(self, frame, reply=None):
        if frame.ID < 0x80000000:
            if frame.sequence_Id is None:
                frame.sequence_Id = self.frm_seq.get_next()
        else:
            if frame.sequence_Id is None and reply is not None:
                frame.sequence_Id = reply.sequence_Id
        self.send_queue.put(frame)

    def reset_environment(self):
        self.cmpp_status = -1
        self.frm_seq.reset()
        self.msg_seq.reset()
        self.cmpp_active_test_last_time = time.time()
        self.send_once_last_time = time.time()

        while not self.send_queue.empty():
            self.send_queue.get()

        for msg in self.commit_resp_wait_list.values():
            self.commit_queue.put((msg.get('sms_obj'), True))
        self.commit_resp_wait_list.clear()

    def cmpp_connect(self):
        sp_id = self.config.cmpp_sp_id.encode()
        sp_pwd = self.config.cmpp_sp_pwd.encode()
        version = (self.config.cmpp_version_1, self.config.cmpp_version_2)
        str_timestamp = time.strftime('%m%d%H%M%S')
        timestamp = long(str_timestamp)
        authenticatorSource = hashlib.md5(sp_id + ('\0' * 9) + sp_pwd + str_timestamp).digest()
        version = version[0] * (1 << 4) + version[1] * (1 ^ 0)

        connect = CMPP2_CONNECT()
        connect.sequence_Id = self.frm_seq.get_next()
        connect.sp_id = sp_id
        connect.authenticatorSource = authenticatorSource
        connect.version = version
        connect.timestamp = timestamp

        frame = connect
        log(
            title='CMPP2_SEND_FRAME_%s_%s_%s' % (
                self.config.cmpp_sp_id.encode(), self.config.cmpp_src_id.encode(),
                Cmpp2FrameHandler.ID_TO_NAME[frame.ID]),
            content=frame.__dict__,
            logger='sms',
            level='debug'
        )
        self.socket_client.send(connect)

        # connect_resp=CMPP2_CONNECT_RESP
        connect_resp = self.socket_client.recv()

        frame = connect_resp
        log(
            title='CMPP2_RECEIVE_FRAME_%s_%s_%s' % (
                self.config.cmpp_sp_id.encode(), self.config.cmpp_src_id.encode(),
                Cmpp2FrameHandler.ID_TO_NAME[frame.ID]),
            content=frame.ID == 0x00000005 and [frame.__dict__, frame.status_report.__dict__] or frame.__dict__,
            logger='sms',
            level='debug'
        )
        return connect_resp.status

    def cmpp_terminate(self):
        terminate = CMPP2_TERMINATE()
        self.send_queue_put(terminate)

    cmpp_active_test_interval = 10

    @keep_interval
    def cmpp_active_test(self):
        active_test = CMPP2_ACTIVE_TEST()
        self.send_queue_put(active_test)

    def commit_resp_wait_list_put(self, seq_id, msg):
        try:
            self.commit_resp_wait_list[seq_id] = msg
        except Exception, _e:
            log(
                title='CMPP2_COMMIT_RESP_WAIT_LIST_PUT_ERROR_%s_%s' % (
                    self.config.cmpp_sp_id.encode(), self.config.cmpp_src_id.encode()),
                content={'msg': [seq_id, msg], 'wait_list': self.commit_resp_wait_list},
                logger='sms',
                level='error'
            )

    def commit_resp_wait_list_get(self, seq_id, raise_error=True):
        try:
            return self.commit_resp_wait_list.pop(seq_id)
        except Exception, _e:
            if raise_error:
                log(
                    title='CMPP2_COMMIT_RESP_WAIT_LIST_GET_ERROR_%s_%s' % (
                        self.config.cmpp_sp_id.encode(), self.config.cmpp_src_id.encode()),
                    content={'msg': [seq_id], 'wait_list': self.commit_resp_wait_list},
                    logger='sms',
                    level='error'
                )

    def submit_one_sms(self):
        if self.commit_queue.qsize() <= 0:
            msg_list = self.task_queue.fetch_sms(count=self.buffer_size)
            for msg in msg_list:
                self.commit_queue.put((msg, True))
            if not msg_list:
                sleep(self.fetch_interval)
                self.send_once_last_time += self.fetch_interval
        if self.commit_queue.qsize() > 0 and len(self.commit_resp_wait_list) < self.wait_size:
            msg, resend = self.commit_queue.get()
            self.cmpp_submit(msg, resend)

    @sms_exception
    def cmpp_submit(self, msg, resend=True):
        # sms_obj=Cmpp2Send
        sms_obj = msg

        cmpp_submit = self.get_cmpp_submit_template()
        msg_content = sms_obj.msg_content.encode(sms_obj.get_msg_fmt_display())
        cmpp_submit = dict(cmpp_submit, **{
            'pk_total': sms_obj.pk_total,
            'pk_number': sms_obj.pk_number,
            'tp_pId': sms_obj.tp_pId,
            'tp_udhi': sms_obj.tp_udhi,
            'registered_delivery': sms_obj.registered_delivery,
            'src_id': sms_obj.src_id.encode(),
            'dest_terminal_id': sms_obj.dest_terminal_id.encode(),
            'msg_fmt': sms_obj.msg_fmt,
            'msg_content': msg_content,
            'msg_length': len(msg_content),
            'sms_obj': sms_obj,
        })

        cmpp_submit_frame = CMPP2_SUBMIT()
        cmpp_submit_frame.msg_id = cmpp_submit.get('msg_id')
        cmpp_submit_frame.pk_total = cmpp_submit.get('pk_total')
        cmpp_submit_frame.pk_number = cmpp_submit.get('pk_number')
        cmpp_submit_frame.registered_delivery = cmpp_submit.get('registered_delivery')
        cmpp_submit_frame.msg_level = cmpp_submit.get('msg_level')
        cmpp_submit_frame.service_id = cmpp_submit.get('service_id')
        cmpp_submit_frame.fee_userType = cmpp_submit.get('fee_userType')
        cmpp_submit_frame.fee_terminal_Id = cmpp_submit.get('fee_terminal_Id')
        cmpp_submit_frame.tp_pId = cmpp_submit.get('tp_pId')
        cmpp_submit_frame.tp_udhi = cmpp_submit.get('tp_udhi')
        cmpp_submit_frame.msg_fmt = cmpp_submit.get('msg_fmt')
        cmpp_submit_frame.msg_src = cmpp_submit.get('msg_src')
        cmpp_submit_frame.feetype = cmpp_submit.get('feetype')
        cmpp_submit_frame.feecode = cmpp_submit.get('feecode')
        cmpp_submit_frame.valid_time = cmpp_submit.get('valid_time')
        cmpp_submit_frame.at_time = cmpp_submit.get('at_time')
        cmpp_submit_frame.src_id = cmpp_submit.get('src_id')
        cmpp_submit_frame.destUsr_tl = cmpp_submit.get('destUsr_tl')
        cmpp_submit_frame.dest_terminal_id = cmpp_submit.get('dest_terminal_id')
        cmpp_submit_frame.msg_length = cmpp_submit.get('msg_length')
        cmpp_submit_frame.msg_content = cmpp_submit.get('msg_content')
        cmpp_submit_frame.reserve = cmpp_submit.get('reserve')

        self.send_queue_put(cmpp_submit_frame)
        self.commit_resp_wait_list_put(cmpp_submit_frame.sequence_Id, cmpp_submit)
        if resend:
            self.submit_timeout(cmpp_submit_frame.sequence_Id, cmpp_submit)
        else:
            self.submit_timeout_2(cmpp_submit_frame.sequence_Id, cmpp_submit)

    submit_timeout_delay = 60

    @gevent_task
    @delay_exec
    def submit_timeout(self, seq_id, msg):
        try:
            msg = self.commit_resp_wait_list_get(seq_id, raise_error=False)
            if msg:
                self.commit_queue.put((msg.get('sms_obj'), False))
        except:
            pass

    @gevent_task
    @delay_exec
    def submit_timeout_2(self, seq_id, msg):
        try:
            msg = self.commit_resp_wait_list_get(seq_id, raise_error=False)
            if msg:
                self.handler.sms_send(self, msg)
        except:
            pass

    def get_cmpp_submit_template(self):
        return {
            'msg_id': 0,
            'pk_total': 1,
            'pk_number': 1,
            'registered_delivery': 0,
            'msg_level': 0,
            'service_id': self.config.cmpp_service_id.encode(),
            'fee_userType': 0,
            'fee_terminal_Id': '',
            'tp_pId': 0,
            'tp_udhi': 0,
            'msg_fmt': 15,
            'msg_src': self.config.cmpp_sp_id.encode(),
            'feetype': '02',
            'feecode': '5',
            'valid_time': '',
            'at_time': '',
            'src_id': self.config.cmpp_src_id.encode(),
            'destUsr_tl': 1,
            'dest_terminal_id': '',
            'msg_length': 0,
            'msg_content': '',
            'reserve': '',
        }


class Cmpp2TerminateException(Exception):
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error


class Cmpp2UnknownCommandIDException(Exception):
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error
