Ext.define('X.model.SuModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'combo', store: 'X.store.UserStore'}
    ]
});