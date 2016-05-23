Ext.define('X.view.PermList', {
    extend: 'X.util.List',

    title: '权限管理',
    model_name: 'X.model.PermModel',
    store_name: 'X.store.PermStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.PermEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.PermEditWindow'},
        {text: '删除', type: 'delete', action: 'base/perm-delete/'}
    ]
});