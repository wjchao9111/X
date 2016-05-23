Ext.define('X.view.UserEditWindow', {
    extend: 'X.util.Window',

    height: 450,
    width: 400,
    base_title: '用户',
    base_url: 'base/user-{0}/',
    model_name: 'X.model.UserModel'
});