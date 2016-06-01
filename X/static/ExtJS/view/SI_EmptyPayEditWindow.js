Ext.define('X.view.SI_EmptyPayEditWindow', {
    extend: 'X.util.Window',

    height: 165,
    width: 400,
    base_title: '报账单号',
    base_url: 'extra/si-emptypay-{0}/',
    model_name: 'X.model.SI_EmptyPayModel'
});