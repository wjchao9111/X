Ext.define('X.model.UserModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'code', label: '账号', show: true, field: 'textfield', regex: re_code},
        {name: 'pwd', label: '密码', field: 'textfield', blank: true, field_cfg: {inputType: 'password'}},
        {
            name: 'pwd_confirm', label: '确认', field: 'textfield', blank: true,
            field_cfg: {inputType: 'password', vtype: 'passConfirm', confirmTo: 'object.pwd', vtypeText: '两次输入密码不一致！'}
        },
        {name: 'name', label: '姓名', show: true, field: 'textfield'},
        {name: 'phone', label: '手机', show: true, field: 'textfield', regex: re_phone},
        {name: 'email', label: '邮箱', show: true, field: 'textfield', regex: re_email},
        {name: 'suffix', label: '扩展码', show: true, field: 'textfield', blank: true, regex: re_suffix},
        {name: 'priority', label: '优先级', field: 'combo', choice: 'user.priority'},
        {name: 'priority_display', label: '优先级', show: true},
        {name: 'stat', label: '状态', field: 'combo', choice: 'user.stat',value:'normal'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'dept_id', label: '归属', field: 'combo', store: 'X.store.DeptStore'},
        {name: 'role_id', label: '角色', field: 'combo', store: 'X.store.RoleStore'},
        {name: 'dept', label: '归属', show: true},
        {name: 'role', label: '角色', show: true}
    ]
});