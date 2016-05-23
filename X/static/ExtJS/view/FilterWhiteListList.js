Ext.define('X.view.FilterWhiteListList', {
    extend: 'X.util.List',

    title: '白名单管理',
    model_name: 'X.model.FilterWhiteListModel',
    store_name: 'X.store.FilterWhiteListStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.FilterWhiteListEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.FilterWhiteListEditWindow'},
        {text: '删除', type: 'delete', action: 'filter/whitelist-delete/'}
    ]
});