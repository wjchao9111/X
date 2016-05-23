Ext.define('X.view.AddrList', {
    extend: 'X.util.List',

    title: '联系人管理',
    model_name: 'X.model.AddrModel',
    store_name: 'X.store.AddrStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.AddrEditWindow'},
        {text: '批量增加', type: 'insert', action: 'X.view.AddrFileWindow'},
        {text: '修改', type: 'update', action: 'X.view.AddrEditWindow'},
        {text: '删除', type: 'delete', action: 'addr/addr-delete/'},
        {text: '导出', type: 'export'}
    ]
});