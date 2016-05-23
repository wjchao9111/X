Ext.define('X.util.Store', {
    extend: 'Ext.data.Store',

    model: null,
    url: null,

    constructor: function (cfg) {
        var me = this;
        cfg = cfg || {};

        var url = me.url;
        if (typeof(url) == 'function') {
            url = url(cfg);
        }

        me.callParent([Ext.apply({
            autoLoad: true,
            pageSize: 20,
            proxy: {
                type: 'ajax',
                actionMethods: {
                    create: 'POST',
                    read: 'POST',
                    update: 'POST',
                    destroy: 'POST'
                },
                url: url,
                filterParam: 'query',
                simpleSortMode: true,
                reader: {
                    type: 'json',
                    root: 'object_list',
                    totalProperty: 'object_count'
                }
            }
        }, cfg)]);
    }
});