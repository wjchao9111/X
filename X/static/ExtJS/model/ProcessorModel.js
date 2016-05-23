Ext.define('X.model.ProcessorModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', field: 'hiddenfield'},
        {name: 'dept_id', label: '企业', field: 'combo', store: 'X.store.DeptStore'},
        {name: 'pid', label: '进程编号', field: 'combo', choice: 'proc.pid'}
    ]
});