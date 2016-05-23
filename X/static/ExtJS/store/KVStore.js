Ext.define('X.store.KVStore', {
    extend: 'Ext.data.Store',
    constructor: function (cfg) {
        var me = this;
        cfg = cfg || {};
        me.type = cfg.type;
        me.data = Ext.decode(kv_data)[me.type];
        me.callParent([Ext.apply({
            data: me.data,
            model: 'X.model.KVModel'
        }, cfg)]);
    }
});