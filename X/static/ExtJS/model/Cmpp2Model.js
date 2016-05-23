Ext.define('X.model.Cmpp2Model', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'sock_source_ip', label: '服务器IP', show: true, field: 'textfield', regex: re_ip, value: '111.11.84.'},
        {name: 'sock_source_port', label: '服务器端口', show: true, field: 'hiddenfield', regex: re_port, value: '0'},
        {name: 'sock_target_ip', label: '网关', show: true, field: 'textfield', regex: re_ip, value: '218.207.67.136'},
        {name: 'sock_target_port', label: '网关端口', show: true, field: 'textfield', regex: re_port, value: '7890'},
        {name: 'cmpp_sp_id', label: '企业代码', show: true, field: 'textfield', regex: re_sp_id},
        {name: 'cmpp_sp_pwd', label: '登陆密码', show: true, field: 'textfield', regex: re_sp_pwd, value: '123456'},
        {name: 'cmpp_src_id', label: '服务代码', show: true, field: 'textfield', regex: re_src_id},
        {name: 'cmpp_service_id', label: '业务代码', show: true, field: 'textfield', regex: re_ser_id, value: 'MHE0010501'},
        {name: 'cmpp_version_1', label: '主版本号', show: true, field: 'hiddenfield', value: '2', regex: re_version},
        {name: 'cmpp_version_2', label: '副版本号', show: true, field: 'hiddenfield', value: '0', regex: re_version},
        {name: 'cmpp_commit_speed', label: '发送速度', show: true, field: 'textfield', regex: re_speed, value: '20'},
        {name: 'cmpp_sign_zh', label: '中文签名', show: true, field: 'textfield'},
        {name: 'cmpp_sign_en', label: '英文签名', show: true, field: 'textfield'},
        {name: 'cmpp_msg_fmt', label: '短信编码', field: 'combo', choice: 'cmpp2.msg_fmt', value: 8},
        {name: 'cmpp_msg_fmt_display', label: '短信编码', show: true},
        {name: 'cmpp_status', label: '端口状态', field: 'combo', choice: 'cmpp2.stat', value: 'enabled'},
        {name: 'cmpp_status_display', label: '端口状态', show: true},
        {name: 'cmpp_ssl', label: '启用SSL', field: 'combo', choice: 'cmpp2.ssl', value: 'disabled'},
        {name: 'cmpp_ssl_display', label: '启用SSL', show: true},
        {name: 'cmpp_dept_id', label: '归属部门', field: 'combo', store: 'X.store.DeptStore'},
        {name: 'cmpp_dept', label: '归属部门', show: true}
    ]
});