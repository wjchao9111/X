Ext.define('X.model.MsgSendModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true},
        {name: 'dest_terminal_id', label: '发送号码', show: true},
        {name: 'src_id', label: '扩展码', show: true},
        {name: 'msg_content', label: '信息内容', show: true},
        {name: 'msg_count', label: '拆分条数', show: true},
        {name: 'msg_stat', label: '发送状态'},
        {name: 'msg_stat_display', label: '发送状态', show: true},
        {name: 'msg_init_time', label: '创建时间', show: true},
        {name: 'msg_send_time', label: '发送时间', show: true},
        {name: 'msg_ack_time', label: '回执时间', show: true},
        {name: 'msg_ack_result', label: '回执内容', show: true},
        {name: 'msg_feed_time', label: '状态报告时间', show: true},
        {name: 'msg_feed_result', label: '状态报告内容', show: true},
        {name: 'registered_delivery', label: '是否获取短信状态报告', show: true},
        {name: 'valid_time', label: '有效时间', show: true},
        {name: 'at_time', label: '定时下发时间', show: true},
        {name: 'msg_user', label: '用户', show: true},
        {name: 'msg_task', label: '任务'}
    ]
});