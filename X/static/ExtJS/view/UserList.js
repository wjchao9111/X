Ext.define('X.view.UserList', {
    extend: 'X.util.List',

    title: '用户管理',
    model_name: 'X.model.UserModel',
    store_name: 'X.store.UserStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.UserEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.UserEditWindow'},
        {text: '删除', type: 'delete', action: 'base/user-delete/'}
    ]
});