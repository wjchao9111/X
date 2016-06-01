Ext.define('X.view.SI_PayUploadWindow', {
    extend: 'X.util.Window',

    height: 165,
    width: 400,
    base_title: '结算报表',
    insert_title: '上传结算报表',
    insert_url: 'extra/si-pay-upload/',
    model_name: 'X.model.SI_PayUploadModel'
});