Ext.define('X.model.FilterAuditModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'name', label: '名称', show: true, field: 'textfield'},
        {name: 'text', label: '内容', show: true, field: 'textareafield', field_cfg: {height: 80}},
        {name: 'note', label: '审核意见', show: true, field: 'textfield'},
        {name: 'regex', label: '正则表达式', field: 'textareafield', field_cfg: {height: 80}},
        {name: 'cmpp_cfg', label: '归属端口', show: true},
        {name: 'stat', label: '状态', field: 'combo', choice: 'filter.stat'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'user', label: '归属用户', show: true}
    ]
});