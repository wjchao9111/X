Ext.define('X.model.AddrGrpModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'name', label: '组名', show: true, field: 'textfield'},
        {name: 'user_id', label: '用户'},
        {name: 'user', label: '用户', show: true},
        {name: 'dept_id', label: '部门'},
        {name: 'dept', label: '部门', show: true},
        {name: 'mod', label: '模式', field: 'combo', choice: 'grp.mod', value: '00'},
        {name: 'mod_display', label: '模式', show: true}
    ]
});