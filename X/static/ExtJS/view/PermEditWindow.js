Ext.define('X.view.PermEditWindow', {
    extend: 'X.util.Window',

    height: 330,
    width: 400,
    base_title: '权限',
    base_url: 'base/perm-{0}/',
    model_name: 'X.model.PermModel'
});