# -*- coding: utf-8 -*-
import copy
import datetime
import re

from X.tools import lazy_loader_const
from X.tools.log import log
from X.tools.model import *
from X.tools.task import *
from filter.models import *
from sms.serv.cmpp2frame import *
from sms.serv.socketlib import *


@lazy_loader_const
@keep_slave_db_alive
def get_white_list_src_id_by_src_id(src_id):
    return [whitelist.src_id for whitelist in WhiteList.objects.filter(src_id__startswith=src_id)]


@lazy_loader_const
@keep_slave_db_alive
def get_filter_regex_list_by_cmpp_cfg(cmpp_cfg):
    return [filter.regex for filter in cmpp_cfg.filter_set.filter(stat='enabled')] + [r'^\d{6}$']


@lazy_loader_const
@keep_slave_db_alive
def get_cmpp2cfg_by_sp_id(sp_id):
    return get_object(Cmpp2Cfg, cmpp_sp_id=sp_id)


class CMPP2_SERVER:
    def __init__(self, serv_addr=('0.0.0.0', 7890,), ssl_mode=False):
        self.ssl_mode = ssl_mode
        if ssl_mode:
            self.serv_sock = SSLServer(serv_addr)
        else:
            self.serv_sock = SocketServer(serv_addr)
        self.start()
        self.session_list = {}
        log(
            title='SERVER_START_LISTEN_%s' % (str(serv_addr)),
            content=None,
            logger='filter',
            level='debug'
        )

    @gevent_task
    def start(self):
        self.serv_sock.listen(backlog=10)
        while True:
            client_sock = self.serv_sock.accept(Cmpp2FrameHandler())
            session = CMPP2_SESSION(self)
            session.accept(client_sock)
            self.push_list(session)

    def push_list(self, session):
        self.session_list[session] = None

    def terminate(self, session):
        self.session_list.pop(session)


class CMPP2_SESSION:
    ID_TO_NAME = {
        0x00000001: 'CMPP2_CONNECT',
        0x80000001: 'CMPP2_CONNECT_RESP',
        0x00000002: 'CMPP2_TERMINATE',
        0x80000002: 'CMPP2_TERMINATE_RESP',
        0x00000004: 'CMPP2_SUBMIT',
        0x80000004: 'CMPP2_SUBMIT_RESP',
        0x00000005: 'CMPP2_DELIVER',
        0x80000005: 'CMPP2_DELIVER_RESP',
        0x00000006: 'CMPP2_QUERY',
        0x80000006: 'CMPP2_QUERY_RESP',
        0x00000007: 'CMPP2_CANCEL',
        0x80000007: 'CMPP2_CANCEL_RESP',
        0x00000008: 'CMPP2_ACTIVE_TEST',
        0x80000008: 'CMPP2_ACTIVE_TEST_RESP'
    }

    def __init__(self, SERVER):
        self.SERVER = SERVER
        self.default_charset = 'gbk'  # 数据库中读取的CMPP2CFG中的unicode数据转化为可以通过socket发送的字符串
        self.client_sock = None  # 作为client与SMG通信的socket
        self.server_sock = None  # 作为server与SP通信的socket
        self.idle = False  # SESSION是否处于空闲状态（等待系统回收资源）
        self.sequence_Id_client = 0  # SESSION的client端向SMG发送消息的seq_id计数器
        self.sequence_Id_server = 0  # SESSION的server端向SP发送消息的seq_id计数器
        self.sequence_Id_msg = 0  # 处理长短信时生成假msg_id时需要使用的seq_id计数器
        self.ISMG_ID = 0  # 处理长短信时生成假msg_id时需要使用的假ISMG编号
        self.sequence_cache_client = {}  # 保存SESSION的client端向SMG发送消息的seq_id=>server收到SP发送消息的seq_id的对应关系，方便产生正确的反向resp。seq_id
        self.sequence_cache_server = {}  # 保存SESSION的server端向SP发送消息的seq_id=>client收到SMG发送消息的seq_id的对应关系，方便产生正确的反向resp。seq_id
        self.sms_merge_cache = {}  # 保存长短信合并临时信息，格式key=frame.src_id+'|'+frame.dest_terminal_id+'|'+str(sms_identity)。value={0:{'sms_pk_total':sms_pk_total,'msg_content':{}},i:frame_i....}
        self.sms_submit_cache = {}  # 处理长短信时生成假msg_id，此处保存submit.seq_id与msg_id的对应关系，方便发送假deliver或转发真deliver时替换frame.msg_Id
        self.sms_msg_id_cache = {}  # 处理长短信时生成假msg_id,此处保存真msg_id与假msg_id的对应关系,以便转发真deliver时替换frame.msg_Id

        self.cmpp_cfg = None
        self.accept_addr = None

    # SESSION的client端向SMG发送消息的seq_id计数器
    def get_sequence_Id_client(self):
        self.sequence_Id_client = (self.sequence_Id_client + 1) % (1 << 32)
        return self.sequence_Id_client % (1 << 32)

        # SESSION的server端向SP发送消息的seq_id计数器

    def get_sequence_Id_server(self):
        self.sequence_Id_server = (self.sequence_Id_server + 1) % (1 << 32)
        return self.sequence_Id_server % (1 << 32)

    # 处理长短信时生成假msg_id时需要使用的seq_id计数器
    def get_sequence_Id_msg(self):
        self.sequence_Id_msg = (self.sequence_Id_msg + 1) % (1 << 16)
        return self.sequence_Id_msg % (1 << 16)

        # 处理长短信时生成假msg_id

    def get_msg_id(self):
        now = datetime.datetime.now()
        msg_id = (now.month << 60) + (now.day << 55) + (now.hour << 50) + (now.minute << 44) + (now.second << 38) + (
            self.ISMG_ID << 16) + (self.get_sequence_Id_msg())
        return msg_id

    # 作为client与网关通信的SEQ管理,生成合适的seq_id
    def set_sequence_Id_client(self, frame, related, force=True):
        if frame.ID < 0x80000000:
            if force or frame.sequence_Id is None:
                frame.sequence_Id = self.get_sequence_Id_client()
                self.sequence_cache_client[frame.sequence_Id] = related
        else:
            if force or frame.sequence_Id is None:
                frame.sequence_Id = self.sequence_cache_server.pop(related.sequence_Id).sequence_Id

    # 作为server与sp通信的SEQ管理,生成合适的seq_id
    def set_sequence_Id_server(self, frame, related, force=True):
        if frame.ID < 0x80000000:
            if force or frame.sequence_Id is None:
                frame.sequence_Id = self.get_sequence_Id_server()
                self.sequence_cache_server[frame.sequence_Id] = related
        else:
            if force or frame.sequence_Id is None:
                frame.sequence_Id = self.sequence_cache_client.pop(related.sequence_Id).sequence_Id

    # 接收server端accepted socket启动SESSION
    @gevent_task
    def accept(self, sock):
        try:
            # 检查accept_addr是否合法
            self.accept_addr = accept_addr = sock.source
            self.server_sock = sock
            connect_frame = CMPP2_CONNECT
            connect_frame = self.server_sock.recv()
            sp_id = connect_frame.sp_id
            cmpp_cfg = get_cmpp2cfg_by_sp_id(sp_id)
            if cmpp_cfg is None:
                self.close()
                log(
                    title='SESSION_BAD_ADDRESS_%s_%s_%s' % (None, None, str(self.accept_addr)),
                    content=None,
                    logger='filter',
                    level='error'
                )
                return None
            self.cmpp_cfg = cmpp_cfg
            if not (accept_addr[0] == cmpp_cfg.sock_accept_ip or
                        cmpp_cfg.sock_accept_ip.startswith(accept_addr[0] + ',') or
                        cmpp_cfg.sock_accept_ip.endswith(',' + accept_addr[0]) or
                        (cmpp_cfg.sock_accept_ip.find(',' + accept_addr[0] + ',') >= 0)
                    ):
                self.close()
                log(
                    title='SESSION_BAD_ADDRESS_%s_%s_%s' % (
                        self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg.cmpp_src_id, str(self.accept_addr)),
                    content=None,
                    logger='filter',
                    level='error'
                )
                return None
            # 向SMG转发CMPP_CONNECT消息
            source = (cmpp_cfg.sock_source_ip.encode(), cmpp_cfg.sock_source_port)
            target = (cmpp_cfg.sock_target_ip.encode(), cmpp_cfg.sock_target_port)
            self.client_sock = SocketClient(source, target, frame_handler=Cmpp2FrameHandler(), name='client')
            self.client_sock.connect()
            self.exec_client_send(connect_frame)
            # 启动client 和 server端消息接收服务
            self.start_client()
            self.start_server()
            log(
                title='SESSION_START_%s_%s_%s' % (
                    self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg.cmpp_src_id, str(self.accept_addr)),
                content=None,
                logger='filter',
                level='debug'
            )
        except:
            self.close()
            log(
                title='SESSION_ACCEPT_UNKNOWN_ERROR_%s_%s_%s' % (
                    self.cmpp_cfg and self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg and self.cmpp_cfg.cmpp_src_id,
                    str(self.accept_addr)),
                content=None,
                logger='filter',
                level='error'
            )

    # 检查submit.content是否合法，src in whitelist视同合法
    def match(self, msg_content, src_id):
        src_id = src_id.replace('\0', '')
        for white_src_id in get_white_list_src_id_by_src_id(self.cmpp_cfg.cmpp_src_id.encode(self.default_charset)):
            if src_id.startswith(white_src_id):
                return True
        for regex in get_filter_regex_list_by_cmpp_cfg(self.cmpp_cfg):
            if re.compile(regex).match(msg_content):
                return True
        log(
            title='FILTER_MATCH_ERROR_%s_%s_%s' % (
                self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg.cmpp_src_id, str((src_id, msg_content))),
            content=None,
            logger='filter',
            level='debug'
        )
        return False

    # 将submit.content编码内容转化为unicode，以便检查其内容
    def sms_decode(self, fmt, data):
        if fmt == 0:  # ascii
            return data.decode('ascii')
        elif fmt == 1:  # writecard
            return ''.join([len(hex(ord(c))) == 3 and '0' + hex(ord(c))[2:] or hex(ord(c))[2:] for c in data])
        elif fmt == 4:  # bin
            return ''.join([len(hex(ord(c))) == 3 and '0' + hex(ord(c))[2:] or hex(ord(c))[2:] for c in data])
        elif fmt == 8:
            return data.decode('UTF-16BE')
        elif fmt == 15:
            return data.decode('gbk')
        return data

    # 筛选submit是否允许转发，返回值：1、True、False、None:长短信未拼接完成，2、当前消息，或合并完成的长短信list
    def filter(self, submit_frame):
        frame = CMPP2_SUBMIT
        frame = submit_frame
        msg_content, frame_obj = self.merge_sms(frame)
        if msg_content is None:
            return None, frame
        return self.match(msg_content, frame.src_id), frame_obj

    # 合并长短信，如果没有拼接完成，返回None,None,如果拼接完成，返回content（unicode），submitlist
    def merge_sms(self, submit_frame):
        frame = CMPP2_SUBMIT
        frame = submit_frame
        if frame.tp_udhi == 0:
            return self.sms_decode(frame.msg_fmt, frame.msg_content), frame
        if frame.msg_content[0] == '\5':
            sms_identity = ord(frame.msg_content[3])
            sms_pk_total = ord(frame.msg_content[4])
            sms_pk_number = ord(frame.msg_content[5])
            msg_content = frame.msg_content[6:]
        else:
            sms_identity = ord(frame.msg_content[3]) * 256 + ord(frame.msg_content[4])
            sms_pk_total = ord(frame.msg_content[5])
            sms_pk_number = ord(frame.msg_content[6])
            msg_content = frame.msg_content[7:]

        key = frame.src_id + '|' + frame.dest_terminal_id + '|' + str(sms_identity)
        if key not in self.sms_merge_cache:
            self.sms_merge_cache[key] = {}
            self.sms_merge_cache[key][0] = {'sms_pk_total': sms_pk_total, 'msg_content': {}}
        self.sms_merge_cache[key][sms_pk_number] = frame
        self.sms_merge_cache[key][0]['msg_content'][sms_pk_number] = msg_content
        if len(self.sms_merge_cache[key]) - 1 < self.sms_merge_cache[key][0]['sms_pk_total']:
            return None, None
        sms_cache_obj = self.sms_merge_cache.pop(key)
        msg_content = ''.join([sms_cache_obj[0]['msg_content'][i + 1] for i in range(sms_cache_obj[0]['sms_pk_total'])])
        frame_list = [sms_cache_obj[i + 1] for i in range(sms_cache_obj[0]['sms_pk_total'])]
        return self.sms_decode(frame.msg_fmt, msg_content), frame_list

    def exec_client_send(self, frame, related=None, force=True):
        if related is None:
            related = copy.copy(frame)
        self.set_sequence_Id_client(frame, related, force)
        if frame.sequence_Id >= 0:
            log(
                title='CLIENT_SEND_FRAME_%s_%s_%s' % (
                    self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg.cmpp_src_id, CMPP2_SESSION.ID_TO_NAME[frame.ID]),
                content=frame.__dict__,
                logger='filter',
                level='debug'
            )
            self.client_sock.send(frame)

    def exec_server_send(self, frame, related=None, force=True):
        if related is None:
            related = copy.copy(frame)
        self.set_sequence_Id_server(frame, related, force)
        if frame.sequence_Id >= 0:
            log(
                title='SERVER_SEND_FRAME_%s_%s_%s' % (
                    self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg.cmpp_src_id, CMPP2_SESSION.ID_TO_NAME[frame.ID]),
                content=frame.__dict__,
                logger='filter',
                level='debug'
            )
            self.server_sock.send(frame)

    def get_fake_submit_resp(self, frame, result):
        submit_frame = frame
        submit_resp = CMPP2_SUBMIT_RESP()
        submit_resp.msg_id = self.get_msg_id()
        submit_resp.result = result
        submit_resp.sequence_Id = submit_frame.sequence_Id
        if result == 10:
            self.sms_submit_cache[submit_frame.sequence_Id] = submit_resp.msg_id
        return submit_resp

    def get_fake_deliver(self, frame):
        submit_frame = frame
        deliver_frame = CMPP2_DELIVER()
        deliver_frame.msg_id = self.get_msg_id()
        deliver_frame.dest_id = submit_frame.src_id
        deliver_frame.service_id = submit_frame.service_id
        deliver_frame.tp_pid = 0
        deliver_frame.tp_udhi = 0
        deliver_frame.msg_fmt = submit_frame.msg_fmt
        deliver_frame.src_terminal_id = submit_frame.dest_terminal_id
        deliver_frame.registered_delivery = 1
        deliver_frame.msg_length = 60
        deliver_frame.status_report = CMPP2_STATUS_REPORT()
        deliver_frame.status_report.msg_id = self.sms_submit_cache.pop(submit_frame.sequence_Id)
        deliver_frame.status_report.stat = 'XF:0011'
        deliver_frame.status_report.submit_time = datetime.datetime.now().strftime('%y%m%d%H%M')
        deliver_frame.status_report.done_time = datetime.datetime.now().strftime('%y%m%d%H%M')
        deliver_frame.status_report.dest_terminal_id = submit_frame.dest_terminal_id
        deliver_frame.status_report.SMSC_sequence = 0  # 不知道填啥
        deliver_frame.reserved = ''
        deliver_frame.sequence_Id = -1
        return deliver_frame

    def server_process_cmpp_submit(self, frame):
        submit_frame = CMPP2_SUBMIT
        submit_frame = frame
        match, frame_obj = self.filter(submit_frame)
        if match is None:
            submit_resp = self.get_fake_submit_resp(submit_frame, 10)  # 假消息，不同步seq_id
            self.exec_server_send(submit_resp, force=False)
            return
        if match:
            if type(frame_obj) == list:
                submit_resp = self.get_fake_submit_resp(submit_frame, 10)
                self.exec_server_send(submit_resp, force=False)  # 假消息，不同步seq_id
                for frm in frame_obj:
                    self.exec_client_send(frm)
            else:
                self.exec_client_send(submit_frame)

        else:
            if type(frame_obj) == list:
                submit_resp = self.get_fake_submit_resp(submit_frame, 10)
                self.exec_server_send(submit_resp, force=False)  # 假消息，不同步seq_id
                for frm in frame_obj:
                    deliver_frame = self.get_fake_deliver(frm)
                    self.exec_server_send(deliver_frame)

            else:
                submit_resp = self.get_fake_submit_resp(submit_frame, 11)
                self.exec_server_send(submit_resp, force=False)

    @gevent_task
    def start_server(self):
        try:
            while True:
                frame = self.server_sock.recv()
                if frame is not None:
                    log(
                        title='SERVER_RECEIVE_FRAME_%s_%s_%s' % (
                            self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg.cmpp_src_id, CMPP2_SESSION.ID_TO_NAME[frame.ID]),
                        content=frame.__dict__,
                        logger='filter',
                        level='debug'
                    )
                    if frame.ID == CMPP2_SUBMIT.ID:
                        self.server_process_cmpp_submit(frame)
                    else:
                        self.exec_client_send(frame)  # 如果此处deliver_resp.seq_id<0,说明是fake_deliver的resp,系统默认不转发

                else:
                    log(
                        title='SERVER_RECEIVE_NONE_%s_%s' % (self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg.cmpp_src_id),
                        content=None,
                        logger='filter',
                        level='debug'
                    )
                    break
        except:
            log(
                title='SERVER_RECEIVE_UNKNOWN_ERROR_%s_%s_%s' % (
                    self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg.cmpp_src_id, str(self.accept_addr)),
                content=None,
                logger='filter',
                level='error'
            )
        finally:
            self.close()

    @gevent_task
    def start_client(self):
        try:
            while True:
                frame = self.client_sock.recv()
                if frame is not None:
                    log(
                        title='CLIENT_RECEIVE_FRAME_%s_%s_%s' % (
                            self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg.cmpp_src_id, CMPP2_SESSION.ID_TO_NAME[frame.ID]),
                        content=frame.ID == 0x00000005 and [frame.__dict__,
                                                            frame.status_report.__dict__] or frame.__dict__,
                        logger='filter',
                        level='debug'
                    )
                    if frame.ID == CMPP2_SUBMIT_RESP.ID:
                        submit_resp_frame = frame
                        self.set_sequence_Id_server(submit_resp_frame, copy.copy(submit_resp_frame))
                        if submit_resp_frame.sequence_Id in self.sms_submit_cache:
                            msg_id = self.sms_submit_cache.pop(submit_resp_frame.sequence_Id)
                            self.sms_msg_id_cache[submit_resp_frame.msg_id] = msg_id
                        else:
                            self.exec_server_send(submit_resp_frame, force=False)
                    elif frame.ID == CMPP2_DELIVER.ID and frame.registered_delivery:
                        deliver_frame = frame
                        if deliver_frame.status_report.msg_id in self.sms_msg_id_cache:
                            msg_id = self.sms_msg_id_cache.pop(deliver_frame.status_report.msg_id)
                            deliver_frame.status_report.msg_id = msg_id
                        self.exec_server_send(deliver_frame)
                    else:
                        self.exec_server_send(frame)
                else:
                    log(
                        title='CLIENT_RECEIVE_TERMINATE_%s_%s' % (self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg.cmpp_src_id),
                        content=frame.__dict__,
                        logger='filter',
                        level='debug'
                    )
                    break
        except:
            log(
                title='CLIENT_RECEIVE_UNKNOWN_ERROR_%s_%s_%s' % (
                    self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg.cmpp_src_id, str(self.accept_addr)),
                content=None,
                logger='filter',
                level='debug'
            )
        finally:
            self.close()

    def close(self):
        self.idle = True
        if self.server_sock:
            self.server_sock.close()
        if self.client_sock:
            self.client_sock.close()
        self.SERVER.terminate(self)
        log(
            title='SESSION_CLOSE_%s_%s_%s' % (
                self.cmpp_cfg and self.cmpp_cfg.cmpp_sp_id, self.cmpp_cfg and self.cmpp_cfg.cmpp_src_id,
                str(self.accept_addr)),
            content=None,
            logger='filter',
            level='debug'
        )
