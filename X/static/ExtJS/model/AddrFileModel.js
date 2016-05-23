Ext.define('X.model.AddrFileModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', field: 'hiddenfield'},
        {name: 'file', label: '文件', field: 'filefield'},
        {name: 'group_id', label: '组', field: 'combo', store: 'X.store.AddrGrpStore'}
    ]
});