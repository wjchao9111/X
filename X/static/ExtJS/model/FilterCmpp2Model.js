Ext.define('X.model.FilterCmpp2Model', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'sock_source_ip', label: '服务器IP', show: true, field: 'textfield', regex: re_ip, value: '111.11.84.'},
        {name: 'sock_source_port', label: '服务器端口', show: true, field: 'hiddenfield', regex: re_port, value: '0'},
        {name: 'sock_target_ip', label: '网关', show: true, field: 'textfield', regex: re_ip, value: '218.207.67.136'},
        {name: 'sock_target_port', label: '网关端口', show: true, field: 'textfield', regex: re_port, value: '7890'},
        {name: 'sock_accept_ip', label: '客户端IP地址', show: true, field: 'textfield', regex: re_ip},
        {name: 'cmpp_sp_id', label: '企业代码', show: true, field: 'textfield', regex: re_sp_id},
        {name: 'cmpp_src_id', label: '服务代码', show: true, field: 'textfield', regex: re_src_id},
        {name: 'cmpp_status', label: '端口状态', field: 'combo', choice: 'filtercmpp2.stat', value: 'enabled'},
        {name: 'cmpp_status_display', label: '端口状态', show: true},
        {name: 'cmpp_dept_id', label: '归属部门', field: 'combo', store: 'X.store.DeptStore'},
        {name: 'cmpp_dept', label: '归属部门', show: true}
    ]
});