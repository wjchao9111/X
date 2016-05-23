Ext.define('X.view.FilterAuditList', {
    extend: 'X.util.List',

    title: '模板管理',
    model_name: 'X.model.FilterModel',
    store_name: 'X.store.FilterStore',
    button_list: [
        {text: '审批', type: 'update', action: 'X.view.FilterAuditWindow'}
    ]
});