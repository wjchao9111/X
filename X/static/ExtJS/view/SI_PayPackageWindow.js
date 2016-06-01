Ext.define('X.view.SI_PayPackageWindow', {
    extend: 'X.util.Window',

    height: 165,
    width: 400,
    base_title: '报帐批次',
    insert_title: '报帐批次新增',
    insert_url: 'extra/si-pay-package-rest/',
    model_name: 'X.model.SI_PayPackageModel'
});