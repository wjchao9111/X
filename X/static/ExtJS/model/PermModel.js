Ext.define('X.model.PermModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'code', label: '编码', show: true, field: 'textfield'},
        {name: 'name', label: '名称', show: true, field: 'textfield'},
        {name: 'value', label: '资源', show: true, field: 'textfield'},
        {name: 'stat', label: '状态', field: 'combo', choice: 'perm.stat', value: 'normal'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'type', label: '类型', field: 'combo', choice: 'perm.type'},
        {name: 'type_display', label: '类型', show: true},
        {name: 'note', label: '备注', show: true, field: 'textfield'},
        {name: 'parent_id', label: '归属', field: 'combo', blank: true, store: 'X.store.PermStore'},
        {name: 'parent', label: '归属', show: true}
    ]
});