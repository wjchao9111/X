Ext.define('X.view.DeptList', {
    extend: 'X.util.List',

    title: '部门管理',
    model_name: 'X.model.DeptModel',
    store_name: 'X.store.DeptStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.DeptEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.DeptEditWindow'},
        {text: '删除', type: 'delete', action: 'base/dept-delete/'}
    ]
});