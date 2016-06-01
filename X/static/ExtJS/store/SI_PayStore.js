Ext.define('X.store.SI_PayStore', {
    extend: 'X.util.Store',

    model: 'X.model.SI_PayModel',
    url: function (cfg) {
        var stat = cfg.stat ? cfg.stat : 'all';
        var contract = cfg.contract ? cfg.contract : null;
        if (contract) {
            return 'extra/si-pay-list/' + stat + '/' + contract + '/';
        }
        else {
            return 'extra/si-pay-list/' + stat + '/';
        }
    }
});