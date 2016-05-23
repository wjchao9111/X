Ext.define('X.store.FilterStore', {
    extend: 'X.util.Store',

    model: 'X.model.FilterModel',
    url: function (cfg) {
        var stat = cfg.stat ? cfg.stat : 'all';
        return 'filter/filter-list/' + stat + '/';
    }
});