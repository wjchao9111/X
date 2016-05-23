Ext.define('X.store.AddrStore', {
    extend: 'X.util.Store',

    model: 'X.model.AddrModel',
    url: function (cfg) {
        var grp_id = cfg.grp_id ? cfg.grp_id : 0;
        return 'addr/addr-list/' + grp_id + '/';
    }
});