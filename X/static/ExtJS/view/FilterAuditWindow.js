Ext.define('X.view.FilterAuditWindow', {
    extend: 'X.util.Window',

    height: 385,
    width: 400,
    base_title: '模板',
    update_title: '审核模板',
    base_url: 'filter/filter-{0}/',
    update_url: 'filter/filter-audit/',
    model_name: 'X.model.FilterAuditModel'
});