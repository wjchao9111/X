Ext.define('X.store.SI_InvoiceStore', {
    extend: 'X.util.Store',

    model: 'X.model.SI_InvoiceModel',
    url: function (cfg) {
        var pay = cfg.pay ? cfg.pay : null;
        if (pay) {
            return 'extra/si-invoice-list/' + pay + '/';
        }
        else {
            return 'extra/si-invoice-list/';
        }
    }
});