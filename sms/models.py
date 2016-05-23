# -*- coding: utf-8 -*-
from django.db import models

from base.models import User, Dept


# Create your models here.
class CarrierSection(models.Model):
    carrier_choices = (('CM', u'中国移动'), ('CU', u'中国联通'), ('CT', u'中国电信'))
    carrier = models.CharField(max_length=50, choices=carrier_choices, verbose_name=u'运营商')
    section = models.CharField(max_length=50, verbose_name=u'号段')

    def __unicode__(self):
        return u'%s' % self.section


class Cmpp2Cfg(models.Model):
    stat_choices = (('enabled', u'启用'), ('disabled', u'停用'),)
    ssl_choices = (('enabled', u'启用'), ('disabled', u'停用'),)
    msg_fmt_choices = ((8, u'UTF-16BE'), (15, u'gbk'),)
    sock_source_ip = models.CharField(max_length=50, verbose_name=u'源IP地址')
    sock_source_port = models.IntegerField(verbose_name=u'源端口')
    sock_target_ip = models.CharField(max_length=50, verbose_name=u'目的IP地址')
    sock_target_port = models.IntegerField(verbose_name=u'目的端口')
    cmpp_sp_id = models.CharField(max_length=50, verbose_name=u'企业代码')
    cmpp_sp_pwd = models.CharField(max_length=50, verbose_name=u'登陆密码')
    cmpp_src_id = models.CharField(max_length=50, verbose_name=u'服务代码')
    cmpp_service_id = models.CharField(max_length=50, verbose_name=u'业务代码')
    cmpp_version_1 = models.IntegerField(verbose_name=u'主版本号')
    cmpp_version_2 = models.IntegerField(verbose_name=u'副版本号')
    cmpp_commit_speed = models.IntegerField(verbose_name=u'发送速度')
    cmpp_sign_zh = models.CharField(max_length=50, verbose_name=u'中文签名')
    cmpp_sign_en = models.CharField(max_length=50, verbose_name=u'英文签名')
    cmpp_msg_fmt = models.IntegerField(choices=msg_fmt_choices, default=15, verbose_name=u'短信编码')
    cmpp_status = models.CharField(max_length=50, choices=stat_choices, verbose_name=u'端口状态')
    cmpp_dept = models.OneToOneField(Dept, related_name='cmpp2cfg', verbose_name=u'归属部门')
    cmpp_ssl = models.CharField(max_length=50, choices=ssl_choices, verbose_name=u'SSL模式')

    def __unicode__(self):
        return u'%s' % self.cmpp_src_id


class QtppCfg(models.Model):
    stat_choices = (('enabled', u'启用'), ('disabled', u'停用'),)
    qtpp_wsdl_url = models.CharField(max_length=100, verbose_name=u'wsdl地址')
    qtpp_si_code = models.CharField(max_length=50, verbose_name=u'SI标识')
    qtpp_service_code = models.CharField(max_length=50, verbose_name=u'业务代码')
    qtpp_ec_code = models.CharField(max_length=50, verbose_name=u'集团编码')
    qtpp_fun_code = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'功能点')
    qtpp_ser_code = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'服务代码')
    qtpp_src_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'源号码')

    qtpp_status = models.CharField(max_length=50, choices=stat_choices, verbose_name=u'端口状态')
    qtpp_dept = models.OneToOneField(Dept, related_name='qtppcfg', verbose_name=u'归属部门')

    def __unicode__(self):
        return u'%s' % self.qtpp_ec_code


class Processor(models.Model):
    pid_choices = ((0, u'Processor 0'),)
    pid = models.IntegerField(default=0, verbose_name=u'进程编号')
    processor_dept = models.OneToOneField(Dept, related_name='processor', verbose_name=u'企业')

    def __unicode__(self):
        return u'%s' % self.pid


class CommonSendTask(models.Model):
    type_choices = (('default', u'普通任务'), ('dynamic', u'动态任务'),)
    stat_choices = (
        ('init', u'已创建'), ('pre.start', u'开始分解'), ('pre.end', u'分解完成'), ('pre.fail', u'分解失败'), ('send.start', u'开始发送'),
        ('send.end', u'发送完成'), ('send.fail', u'发送失败'), ('cancel', u'取消发送'),)
    priority_choices = User.priority_choices
    user = models.ForeignKey(User, verbose_name=u'用户')
    type = models.CharField(max_length=50, choices=type_choices, default='default', verbose_name=u'任务类型')
    name = models.CharField(max_length=50, verbose_name=u'任务名称')
    stat = models.CharField(max_length=50, choices=stat_choices, default='init', verbose_name=u'任务状态')
    pause = models.BooleanField(default=False, verbose_name=u'任务暂停')

    init = models.DateTimeField(auto_now_add=True, verbose_name=u'新建时间')
    timing = models.DateTimeField(null=True, blank=True, verbose_name=u'定时下发时间')
    ending = models.DateTimeField(null=True, blank=True, verbose_name=u'定时停止时间')

    suffix = models.CharField(null=True, blank=True, max_length=50, verbose_name=u'扩展码')
    priority = models.IntegerField(default=9, choices=priority_choices, verbose_name=u'优先级')

    content = models.CharField(max_length=1000, verbose_name=u'短信内容')
    phones = models.CharField(null=True, blank=True, max_length=2000, verbose_name=u'发送号码')
    groups = models.CharField(null=True, blank=True, max_length=200, verbose_name=u'发送通讯录组')
    file = models.FileField(null=True, blank=True, max_length=50, upload_to='addr', verbose_name=u'发送文件')

    count = models.IntegerField(default=-1, verbose_name=u'号码数量')
    submit = models.IntegerField(default=0, verbose_name=u'已提交数量')
    success = models.IntegerField(default=0, verbose_name=u'成功数量')
    error = models.IntegerField(default=0, verbose_name=u'失败数量')
    access = models.DateTimeField(auto_now_add=True, verbose_name=u'最后访问时间')

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s|%s' % (self.id, self.name)


class CommonMsgSend(models.Model):
    stat_choices = (('init', '已创建'), ('fetch', '已读取'), ('send', '已发送'), ('ack', '已提交网关'), ('ack.success', '已提交网关'),
                    ('ack.failed', '提交网关失败'), ('feed', '已获取状态报告'), ('feed.success', '发送成功'), ('feed.failed', '发送失败'),)
    registered_delivery = models.IntegerField(verbose_name=u'是否获取短信回执')
    valid_time = models.DateTimeField(null=True, blank=True, verbose_name=u'有效时间')
    at_time = models.DateTimeField(null=True, blank=True, verbose_name=u'定时下发时间')
    src_id = models.CharField(max_length=50, verbose_name=u'扩展码')
    dest_terminal_id = models.CharField(max_length=100, db_index=True, verbose_name=u'发送号码')
    channle_cfg = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'发送通道')
    msg_content = models.CharField(max_length=1000, null=True, blank=True, verbose_name=u'发送内容')
    msg_count = models.IntegerField(default=0, verbose_name=u'短信条数')
    msg_variable = models.CharField(max_length=1000, null=True, blank=True, verbose_name=u'变量内容')

    msg_init_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    msg_send_time = models.DateTimeField(null=True, blank=True, verbose_name=u'发送时间')
    msg_ack_time = models.DateTimeField(null=True, blank=True, verbose_name=u'回执时间')
    msg_ack_result = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'回执内容')
    msg_feed_time = models.DateTimeField(null=True, blank=True, verbose_name=u'状态报告时间')
    msg_feed_result = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'状态报告内容')
    msg_stat = models.CharField(max_length=50, choices=stat_choices, default='init', db_index=True,
                                verbose_name=u'发送状态')

    msg_user = models.ForeignKey(User, verbose_name=u'用户')

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s|%s' % (self.id, self.dest_terminal_id)


class CommonSmsSend(models.Model):
    stat_choices = (('init', '已创建'), ('fetch', '已读取'), ('send', '已发送'), ('ack', '已提交网关'), ('feed', '已获取状态报告'),)
    sms_init_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    sms_send_time = models.DateTimeField(null=True, blank=True, verbose_name=u'发送时间')
    sms_ack_time = models.DateTimeField(null=True, blank=True, verbose_name=u'回执时间')
    sms_ack_result = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'回执结果')
    sms_done_time = models.DateTimeField(null=True, blank=True, verbose_name=u'状态报告时间')
    sms_feed_time = models.DateTimeField(null=True, blank=True, verbose_name=u'状态报告时间')
    sms_feed_result = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'状态报告内容')
    sms_stat = models.CharField(max_length=50, choices=stat_choices, default='init', db_index=True,
                                verbose_name=u'发送状态')
    sms_user = models.ForeignKey(User, verbose_name=u'用户')

    class Meta:
        abstract = True


class CommonCmpp2Send(CommonSmsSend):
    msg_id = models.CharField(max_length=50, null=True, blank=True, db_index=True, verbose_name=u'信息标识')
    pk_total = models.IntegerField(default=1, verbose_name=u'相同MSGID信息总条数')
    pk_number = models.IntegerField(default=1, verbose_name=u'相同MSGID信息序号')
    registered_delivery = models.IntegerField(default=0, verbose_name=u'是否获取短信回执')
    msg_level = models.IntegerField(default=0, verbose_name=u'信息级别')
    service_id = models.CharField(max_length=50, verbose_name=u'业务代码')
    fee_userType = models.IntegerField(default=0, verbose_name=u'计费用户类型')
    fee_terminal_Id = models.CharField(max_length=50, blank=True, default='', verbose_name=u'被计费用户号码')
    tp_pId = models.IntegerField(default=0, verbose_name=u'GSM协议类型')
    tp_udhi = models.IntegerField(default=0, verbose_name=u'GSM协议类型')
    msg_fmt = models.IntegerField(default=15, choices=Cmpp2Cfg.msg_fmt_choices, verbose_name=u'信息格式')
    msg_src = models.CharField(max_length=50, verbose_name=u'信息内容来源')
    feetype = models.CharField(max_length=50, default='02', verbose_name=u'资费类别')
    feecode = models.CharField(max_length=50, default='5', verbose_name=u'资费代码')
    valid_time = models.DateTimeField(null=True, blank=True, verbose_name=u'存活有效期')
    at_time = models.DateTimeField(null=True, blank=True, verbose_name=u'定时发送时间')
    src_id = models.CharField(max_length=50, verbose_name=u'源号码')
    destUsr_tl = models.IntegerField(verbose_name=u'接收信息用户数量')
    dest_terminal_id = models.CharField(max_length=2100, verbose_name=u'接收短信号码')
    msg_length = models.IntegerField(verbose_name=u'信息长度')
    msg_content = models.CharField(max_length=160, verbose_name=u'信息内容')
    reserve = models.CharField(max_length=50, blank=True, default='', verbose_name=u'保留')

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s|%s' % (self.id, self.dest_terminal_id)


class CommonQtppSend(CommonSmsSend):
    msg_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'信息标识')
    si_code = models.CharField(max_length=50, verbose_name=u'si标识')
    service_code = models.CharField(max_length=50, verbose_name=u'业务代码')
    ec_code = models.CharField(max_length=50, verbose_name=u'集团编号')
    fun_code = models.CharField(max_length=50, null=True, blank=True, default='', verbose_name=u'功能点')
    ser_code = models.CharField(max_length=50, null=True, blank=True, default='', verbose_name=u'服务代码')
    src_id = models.CharField(max_length=50, null=True, blank=True, default='', verbose_name=u'源号码')
    mobile = models.CharField(max_length=50, verbose_name=u'手机号码')
    content = models.CharField(max_length=400, verbose_name=u'手机号码')
    msg_length = models.IntegerField(null=True, verbose_name=u'信息长度')

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s|%s' % (self.id, self.mobile)


class SendTask(CommonSendTask):
    pass


class MsgSend(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask, related_name='msgsend_set', verbose_name=u'任务')


class Cmpp2Send(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend, related_name='cmpp2send_set', verbose_name=u'完整消息')


class QtppSend(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend, related_name='qtppsend_set', verbose_name=u'完整消息')


class MsgRecv(models.Model):
    dest_id = models.CharField(max_length=50, verbose_name=u'目的号码')
    src_terminal_id = models.CharField(max_length=50, verbose_name=u'源终端号码')
    msg_content = models.CharField(max_length=1000, verbose_name=u'信息内容')

    msg_recv_time = models.DateTimeField(verbose_name=u'接收时间')

    msg_user = models.ForeignKey(User, verbose_name=u'用户')

    def __unicode__(self):
        return u'%s|%s' % (self.id, self.dest_id)


class Cmpp2Recv(models.Model):
    msg_id = models.CharField(max_length=50, verbose_name=u'信息标识')
    dest_id = models.CharField(max_length=50, verbose_name=u'目的号码')
    service_id = models.CharField(max_length=50, verbose_name=u'业务代码')
    tp_pid = models.IntegerField(verbose_name=u'GSM协议类型')
    tp_udhi = models.IntegerField(verbose_name=u'GSM协议类型')
    msg_fmt = models.IntegerField(verbose_name=u'信息格式')
    src_terminal_id = models.CharField(max_length=50, verbose_name=u'源终端号码')
    registered_delivery = models.IntegerField(verbose_name=u'是否为状态报告')
    msg_length = models.IntegerField(verbose_name=u'信息长度')
    msg_content = models.CharField(max_length=160, verbose_name=u'信息内容')
    reserved = models.CharField(max_length=50, verbose_name=u'保留')

    sms_identity = models.IntegerField(verbose_name=u'识别码')
    sms_pk_total = models.IntegerField(verbose_name=u'相同MSGID信息总条数')
    sms_pk_number = models.IntegerField(verbose_name=u'相同MSGID信息序号')
    sms_recv_time = models.DateTimeField(auto_now_add=True, verbose_name=u'接收时间')

    sms_user = models.ForeignKey(User, verbose_name=u'用户')
    sms_msg = models.ForeignKey(MsgRecv, related_name='cmpp2_set', null=True, blank=True, verbose_name=u'任务')

    def __unicode__(self):
        return u'%s|%s' % (self.id, self.dest_id)


##########################################################
class SendTask01(CommonSendTask):
    pass


class SendTask02(CommonSendTask):
    pass


class SendTask03(CommonSendTask):
    pass


class SendTask04(CommonSendTask):
    pass


class SendTask05(CommonSendTask):
    pass


class SendTask06(CommonSendTask):
    pass


class SendTask07(CommonSendTask):
    pass


class SendTask08(CommonSendTask):
    pass


class SendTask09(CommonSendTask):
    pass


class SendTask10(CommonSendTask):
    pass


class SendTask11(CommonSendTask):
    pass


class SendTask12(CommonSendTask):
    pass


class MsgSend01(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask01, related_name='msgsend_set', verbose_name=u'任务')


class MsgSend02(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask02, related_name='msgsend_set', verbose_name=u'任务')


class MsgSend03(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask03, related_name='msgsend_set', verbose_name=u'任务')


class MsgSend04(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask04, related_name='msgsend_set', verbose_name=u'任务')


class MsgSend05(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask05, related_name='msgsend_set', verbose_name=u'任务')


class MsgSend06(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask06, related_name='msgsend_set', verbose_name=u'任务')


class MsgSend07(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask07, related_name='msgsend_set', verbose_name=u'任务')


class MsgSend08(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask08, related_name='msgsend_set', verbose_name=u'任务')


class MsgSend09(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask09, related_name='msgsend_set', verbose_name=u'任务')


class MsgSend10(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask10, related_name='msgsend_set', verbose_name=u'任务')


class MsgSend11(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask11, related_name='msgsend_set', verbose_name=u'任务')


class MsgSend12(CommonMsgSend):
    msg_task = models.ForeignKey(SendTask12, related_name='msgsend_set', verbose_name=u'任务')


class Cmpp2Send01(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask01, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend01, related_name='cmpp2send_set', verbose_name=u'完整消息')


class Cmpp2Send02(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask02, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend02, related_name='cmpp2send_set', verbose_name=u'完整消息')


class Cmpp2Send03(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask03, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend03, related_name='cmpp2send_set', verbose_name=u'完整消息')


class Cmpp2Send04(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask04, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend04, related_name='cmpp2send_set', verbose_name=u'完整消息')


class Cmpp2Send05(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask05, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend05, related_name='cmpp2send_set', verbose_name=u'完整消息')


class Cmpp2Send06(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask06, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend06, related_name='cmpp2send_set', verbose_name=u'完整消息')


class Cmpp2Send07(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask07, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend07, related_name='cmpp2send_set', verbose_name=u'完整消息')


class Cmpp2Send08(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask08, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend08, related_name='cmpp2send_set', verbose_name=u'完整消息')


class Cmpp2Send09(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask09, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend09, related_name='cmpp2send_set', verbose_name=u'完整消息')


class Cmpp2Send10(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask10, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend10, related_name='cmpp2send_set', verbose_name=u'完整消息')


class Cmpp2Send11(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask11, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend11, related_name='cmpp2send_set', verbose_name=u'完整消息')


class Cmpp2Send12(CommonCmpp2Send):
    sms_task = models.ForeignKey(SendTask12, related_name='cmpp2send_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend12, related_name='cmpp2send_set', verbose_name=u'完整消息')


class QtppSend01(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask01, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend01, related_name='qtppsend_set', verbose_name=u'完整消息')


class QtppSend02(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask02, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend02, related_name='qtppsend_set', verbose_name=u'完整消息')


class QtppSend03(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask03, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend03, related_name='qtppsend_set', verbose_name=u'完整消息')


class QtppSend04(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask04, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend04, related_name='qtppsend_set', verbose_name=u'完整消息')


class QtppSend05(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask05, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend05, related_name='qtppsend_set', verbose_name=u'完整消息')


class QtppSend06(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask06, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend06, related_name='qtppsend_set', verbose_name=u'完整消息')


class QtppSend07(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask07, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend07, related_name='qtppsend_set', verbose_name=u'完整消息')


class QtppSend08(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask08, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend08, related_name='qtppsend_set', verbose_name=u'完整消息')


class QtppSend09(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask09, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend09, related_name='qtppsend_set', verbose_name=u'完整消息')


class QtppSend10(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask10, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend10, related_name='qtppsend_set', verbose_name=u'完整消息')


class QtppSend11(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask11, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend11, related_name='qtppsend_set', verbose_name=u'完整消息')


class QtppSend12(CommonQtppSend):
    sms_task = models.ForeignKey(SendTask12, related_name='qtppsend_set', verbose_name=u'任务')
    sms_msg = models.ForeignKey(MsgSend12, related_name='qtppsend_set', verbose_name=u'完整消息')
