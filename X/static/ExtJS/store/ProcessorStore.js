Ext.define('X.store.ProcessorStore', {
    extend: 'X.util.Store',

    model: 'X.model.DeptModel',
    url: function (cfg) {
        var pid = cfg.pid >= 0 ? cfg.pid : -1;
        return pid >= 0 ? 'sms/processor-list-' + pid + '/' : 'sms/processor-list/';
    }
});