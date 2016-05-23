Ext.define('X.view.DeptEditWindow', {
    extend: 'X.util.Window',

    height: 220,
    width: 400,
    base_title: '部门',
    base_url: 'base/dept-{0}/',
    model_name: 'X.model.DeptModel'
});