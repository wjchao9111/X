Ext.define('X.model.AddrModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'phone', label: '手机', show: true, field: 'textfield', regex: re_phone},
        {name: 'name', label: '姓名', show: true, field: 'textfield'},
        {name: 'sex', label: '性别', show: true, field: 'combo', blank: true, choice: 'addr.sex'},
        {name: 'email', label: '邮箱', show: true, field: 'textfield', blank: true, regex: re_email},
        {name: 'company', label: '公司', show: true, field: 'textfield', blank: true},
        {name: 'dept', label: '部门', show: true, field: 'textfield', blank: true},
        {name: 'post', label: '邮编', show: true, field: 'textfield', blank: true},
        {name: 'addr', label: '地址', show: true, field: 'textfield', blank: true},
        {name: 'group_id', label: '组名', field: 'combo', store: 'X.store.AddrGrpStore'},
        {name: 'group', label: '组名', show: true}
    ]
});