Ext.define('X.view.ApiUserList', {
    extend: 'X.util.List',

    title: '接口用户管理',
    model_name: 'X.model.UserModel',
    store_name: 'X.store.ApiUserStore',
    button_list: []
});