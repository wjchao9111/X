Ext.define('X.view.SI_InvoiceEditWindow', {
    extend: 'X.util.Window',

    height: 550,
    width: 400,
    base_title: '发票',
    base_url: 'extra/si-invoice-{0}/',
    model_name: 'X.model.SI_InvoiceModel'
});