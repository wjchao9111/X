Ext.define('X.view.WxltEditWindow', {
    extend: 'X.util.Window',

    height: 275,
    width: 400,
    base_title: 'WXLT接口',
    base_url: 'sms/wxlt-{0}/',
    model_name: 'X.model.WxltModel'
});