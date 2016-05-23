Ext.define('X.model.DeptModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'name', label: '名称', show: true, field: 'textfield'},
        {name: 'stat', label: '状态', field: 'combo', value: 'normal', choice: 'dept.stat'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'type', label: '类型'},
        {name: 'type_display', label: '类型', show: true},
        {name: 'parent_id', label: '归属', field: 'combo', store: 'X.store.DeptStore', blank: true},
        {name: 'parent', label: '归属', show: true}
    ]
});