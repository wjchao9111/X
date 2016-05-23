Ext.define('X.model.UserResetPassModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'code', label: '账号', show: true, field: 'hiddenfield'},
        {name: 'old_pwd', label: '旧密码', field: 'textfield', field_cfg: {inputType: 'password'}},
        {name: 'pwd', label: '新密码', field: 'textfield', field_cfg: {inputType: 'password'}},
        {
            name: 'pwd_confirm', label: '确认', field: 'textfield',
            field_cfg: {inputType: 'password', vtype: 'passConfirm', confirmTo: 'object.pwd', vtypeText: '两次输入密码不一致！'}
        }
    ]
});