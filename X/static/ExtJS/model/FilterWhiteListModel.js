Ext.define('X.model.FilterWhiteListModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'src_id', label: '服务代码', show: true, field: 'textfield', regex: re_src_id},
        {name: 'name', label: '名称', show: true, field: 'textfield'}
    ]
});