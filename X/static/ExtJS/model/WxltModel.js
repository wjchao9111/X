Ext.define('X.model.WxltModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'pinid', label: 'pinid', show: true, field: 'textfield'},
        {name: 'accountid', label: '账号', show: true, field: 'textfield'},
        {name: 'accountpwd', label: '密码', show: true, field: 'textfield'},
        {name: 'des_key', label: '密钥', show: true, field: 'textfield'},
        {name: 'dept_user_id', label: '用户', field: 'combo', store: 'X.store.WxltUserStore'},
        {name: 'dept_user', label: '用户', show: true}
    ]
});