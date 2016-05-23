Ext.define('X.view.RoleList', {
    extend: 'X.util.List',

    title: '角色管理',
    model_name: 'X.model.RoleModel',
    store_name: 'X.store.RoleStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.RoleEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.RoleEditWindow'},
        {text: '删除', type: 'delete', action: 'base/role-delete/'},
        {text: '权限', type: 'update', action: 'X.view.RolePermWindow'}
    ]
});