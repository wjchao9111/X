Ext.define('X.model.RoleModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'name', label: '名称', show: true, field: 'textfield'},
        {name: 'type', label: '类型'},
        {name: 'type_display', label: '类型', show: true},
        {name: 'stat', label: '状态', field: 'combo', choice: 'role.stat', value: 'normal'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'dept_id', label: '归属'},
        {name: 'dept', label: '归属', show: true}
    ]
});