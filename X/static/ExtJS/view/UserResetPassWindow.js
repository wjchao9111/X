Ext.define('X.view.UserResetPassWindow', {
    extend: 'X.util.Window',

    height: 200,
    width: 400,
    base_title: '用户',
    update_title: '修改用户密码',
    update_url: 'base/user-reset-pass/',
    model_name: 'X.model.UserResetPassModel'
});