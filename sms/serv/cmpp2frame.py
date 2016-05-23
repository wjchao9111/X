# -*- coding: utf-8 -*-

import struct
from sms.serv.socketlib import SocketFrameHandler


class CMPP2_CONNECT:
    ID = 0x00000001

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None
        self.sp_id = None
        self.authenticatorSource = None
        self.version = None
        self.timestamp = None

    def get_format(self):
        return '!3L6s16sBL'

    def get_length(self):
        return 12 + 27

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
            self.sp_id,
            self.authenticatorSource,
            self.version,
            self.timestamp
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id,
            self.sp_id,
            self.authenticatorSource,
            self.version,
            self.timestamp
        ) = struct.unpack(self.get_format(), data)


class CMPP2_CONNECT_RESP:
    ID = 0x80000001

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None
        self.status = None
        self.authenticatorISMG = None
        self.version = None

    def get_format(self, ):
        return '!3LB16sB'

    def get_length(self):
        return 12 + 18

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
            self.status,
            self.authenticatorISMG,
            self.version,
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id,
            self.status,
            self.authenticatorISMG,
            self.version
        ) = struct.unpack(self.get_format(), data)


class CMPP2_TERMINATE:
    ID = 0x00000002

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None

    def get_format(self):
        return '!3L'

    def get_length(self):
        return 12

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id
        ) = struct.unpack(self.get_format(), data)


class CMPP2_TERMINATE_RESP:
    ID = 0x80000002

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None

    def get_format(self):
        return '!3L'

    def get_length(self):
        return 12

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id
        ) = struct.unpack(self.get_format(), data)


class CMPP2_SUBMIT:
    ID = 0x00000004

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None
        self.msg_id = None
        self.pk_total = None
        self.pk_number = None
        self.registered_delivery = None
        self.msg_level = None
        self.service_id = None
        self.fee_userType = None
        self.fee_terminal_Id = None
        self.tp_pId = None
        self.tp_udhi = None
        self.msg_fmt = None
        self.msg_src = None
        self.feetype = None
        self.feecode = None
        self.valid_time = None
        self.at_time = None
        self.src_id = None
        self.destUsr_tl = None
        self.dest_terminal_id = None
        self.msg_length = None
        self.msg_content = None
        self.reserve = None

    def get_format(self):
        return '!3LQ4B10sB21s3B6s2s6s17s17s21sB%dsB%ds8s' % (21 * self.destUsr_tl, self.msg_length)

    def get_length(self):
        return 12 + 126 + 21 * self.destUsr_tl + self.msg_length

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
            self.msg_id,
            self.pk_total,
            self.pk_number,
            self.registered_delivery,
            self.msg_level,
            self.service_id,
            self.fee_userType,
            self.fee_terminal_Id,
            self.tp_pId,
            self.tp_udhi,
            self.msg_fmt,
            self.msg_src,
            self.feetype,
            self.feecode,
            self.valid_time,
            self.at_time,
            self.src_id,
            self.destUsr_tl,
            self.dest_terminal_id,
            self.msg_length,
            self.msg_content,
            self.reserve,
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id,
            self.msg_id,
            self.pk_total,
            self.pk_number,
            self.registered_delivery,
            self.msg_level,
            self.service_id,
            self.fee_userType,
            self.fee_terminal_Id,
            self.tp_pId,
            self.tp_udhi,
            self.msg_fmt,
            self.msg_src,
            self.feetype,
            self.feecode,
            self.valid_time,
            self.at_time,
            self.src_id,
            self.destUsr_tl,
        ) = struct.unpack('!3LQ4B10sB21s3B6s2s6s17s17s21sB', data[:129])

        data = data[129:]
        (
            self.dest_terminal_id,
            self.msg_length,
        ) = struct.unpack('!%dsB' % (21 * self.destUsr_tl,), data[:21 * self.destUsr_tl + 1])

        data = data[21 * self.destUsr_tl + 1:]

        (
            self.msg_content,
            self.reserve,
        ) = struct.unpack('!%ds8s' % (self.msg_length,), data)


class CMPP2_SUBMIT_RESP:
    ID = 0x80000004

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None
        self.msg_id = None
        self.result = None

    def get_format(self):
        return '!3LQB'

    def get_length(self):
        return 12 + 9

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
            self.msg_id,
            self.result
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id,
            self.msg_id,
            self.result
        ) = struct.unpack(self.get_format(), data)


class CMPP2_DELIVER:
    ID = 0x00000005

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None
        self.msg_id = None
        self.dest_id = None
        self.service_id = None
        self.tp_pid = None
        self.tp_udhi = None
        self.msg_fmt = None
        self.src_terminal_id = None
        self.registered_delivery = None
        self.msg_length = None
        self.msg_content = None
        self.reserved = None
        self.status_report = CMPP2_STATUS_REPORT()

    def get_format(self):
        return '!3LQ21s10s3B21s2B%ds8s' % self.msg_length

    def get_length(self):
        return 12 + 73 + self.msg_length

    def pack(self):
        if self.registered_delivery:
            self.msg_length = 60
            self.msg_content = self.status_report.pack()

        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
            self.msg_id,
            self.dest_id,
            self.service_id,
            self.tp_pid,
            self.tp_udhi,
            self.msg_fmt,
            self.src_terminal_id,
            self.registered_delivery,
            self.msg_length,
            self.msg_content,
            self.reserved,
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        total_length, = struct.unpack('!L', data[:4])
        msg_length = total_length - 12 - 73
        fmt = '!3LQ21s10s3B21s2B' + str(msg_length) + 's8s'
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id,
            self.msg_id,
            self.dest_id,
            self.service_id,
            self.tp_pid,
            self.tp_udhi,
            self.msg_fmt,
            self.src_terminal_id,
            self.registered_delivery,
            self.msg_length,
            self.msg_content,
            self.reserved) = struct.unpack(fmt, data)

        if self.registered_delivery:
            self.status_report = CMPP2_STATUS_REPORT()
            self.status_report.unpack(self.msg_content)


class CMPP2_DELIVER_RESP:
    ID = 0x80000005

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None
        self.msg_id = None
        self.result = None

    def get_format(self):
        return '!3LQB'

    def get_length(self):
        return 12 + 9

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
            self.msg_id,
            self.result
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id,
            self.msg_id,
            self.result
        ) = struct.unpack(self.get_format(), data)


class CMPP2_QUERY:
    ID = 0x00000006

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None
        self.query_type = None
        self.query_code = None
        self.reserve = None

    def get_format(self):
        return '!3L8sB10s8s'

    def get_length(self):
        return 12 + 27

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
            self.query_type,
            self.query_code,
            self.reserve
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id,
            self.query_type,
            self.query_code,
            self.reserve
        ) = struct.unpack(self.get_format(), data)


class CMPP2_QUERY_RESP:
    ID = 0x80000006

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None
        self.time = None
        self.query_type = None
        self.query_code = None
        self.mt_tlmsg = None
        self.mt_tlusr = None
        self.mt_scs = None
        self.mt_wt = None
        self.mt_fl = None
        self.mt_scs = None
        self.mt_wt = None
        self.mt_fl = None

    def get_format(self):
        return '!3L8sB10s8L'

    def get_length(self):
        return 12 + 51

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
            self.time,
            self.query_type,
            self.query_code,
            self.mt_tlmsg,
            self.mt_tlusr,
            self.mt_scs,
            self.mt_wt,
            self.mt_fl,
            self.mt_scs,
            self.mt_wt,
            self.mt_fl
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id,
            self.time,
            self.query_type,
            self.query_code,
            self.mt_tlmsg,
            self.mt_tlusr,
            self.mt_scs,
            self.mt_wt,
            self.mt_fl,
            self.mt_scs,
            self.mt_wt,
            self.mt_fl
        ) = struct.unpack(self.get_format(), data)


class CMPP2_CANCEL:
    ID = 0x00000007

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None
        self.msg_id = None

    def get_format(self):
        return '!3LQ'

    def get_length(self):
        return 12 + 8

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
            self.msg_id,
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id,
            self.msg_id
        ) = struct.unpack(self.get_format(), data)


class CMPP2_CANCEL_RESP:
    ID = 0x80000007

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None
        self.success_id = None

    def get_format(self):
        return '!3LB'

    def get_length(self):
        return 12 + 1

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
            self.success_id,
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id,
            self.success_id
        ) = struct.unpack(self.get_format(), data)


class CMPP2_ACTIVE_TEST:
    ID = 0x00000008

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None

    def get_format(self):
        return '!3L'

    def get_length(self):
        return 12

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id
        ) = struct.unpack(self.get_format(), data)


class CMPP2_ACTIVE_TEST_RESP:
    ID = 0x80000008

    def __init__(self):
        self.total_length = None
        self.command_Id = None
        self.sequence_Id = None
        self.reserve = None

    def get_format(self):
        return '!3LB'

    def get_length(self):
        return 12 + 1

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.get_length(),
            self.ID,
            self.sequence_Id,
            self.reserve,
        )
        self.command_Id = self.ID
        self.total_length = self.get_length()
        return data

    def unpack(self, data):
        (
            self.total_length,
            self.command_Id,
            self.sequence_Id,
            self.reserve
        ) = struct.unpack(self.get_format(), data)


class CMPP2_STATUS_REPORT:
    def __init__(self):
        self.msg_id = None
        self.stat = None
        self.submit_time = None
        self.done_time = None
        self.dest_terminal_id = None
        self.SMSC_sequence = None

    def get_format(self):
        return '!Q7s10s10s21sL'

    def get_length(self):
        return 60

    def pack(self):
        data = struct.pack(
            self.get_format(),
            self.msg_id,
            self.stat,
            self.submit_time,
            self.done_time,
            self.dest_terminal_id,
            self.SMSC_sequence,
        )
        return data

    def unpack(self, data):
        (
            self.msg_id,
            self.stat,
            self.submit_time,
            self.done_time,
            self.dest_terminal_id,
            self.SMSC_sequence,
        ) = struct.unpack(self.get_format(), data)


class Cmpp2FrameHandler(SocketFrameHandler):
    CMPP_FRAME = {
        0x00000001: CMPP2_CONNECT,
        0x80000001: CMPP2_CONNECT_RESP,
        0x00000002: CMPP2_TERMINATE,
        0x80000002: CMPP2_TERMINATE_RESP,
        0x00000004: CMPP2_SUBMIT,
        0x80000004: CMPP2_SUBMIT_RESP,
        0x00000005: CMPP2_DELIVER,
        0x80000005: CMPP2_DELIVER_RESP,
        0x00000006: CMPP2_QUERY,
        0x80000006: CMPP2_QUERY_RESP,
        0x00000007: CMPP2_CANCEL,
        0x80000007: CMPP2_CANCEL_RESP,
        0x00000008: CMPP2_ACTIVE_TEST,
        0x80000008: CMPP2_ACTIVE_TEST_RESP
    }

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

    def __init__(self):
        SocketFrameHandler.__init__(self)

    def recv_frame(self, data):
        if len(data) < 12:
            return None, data
        total_length, command_Id = struct.unpack('!2L', data[:8])
        if len(data) < total_length:
            return None, data
        return self.recv_cmpp2_frame(data[:total_length], command_Id), data[total_length:]

    def recv_cmpp2_frame(self, data, command_Id):
        FrameClass = Cmpp2FrameHandler.CMPP_FRAME[command_Id]
        frame = FrameClass()
        frame.unpack(data)
        return frame

    def send_frame(self, frame):
        return frame.pack()
