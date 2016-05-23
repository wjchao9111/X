Ext.define('X.model.MsgRecvModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true},
        {name: 'dest_id', label: '端口号', show: true},
        {name: 'src_terminal_id', label: '手机号码', show: true},
        {name: 'msg_content', label: '信息内容', show: true},
        {name: 'msg_recv_time', label: '接收时间', show: true}
    ]
});