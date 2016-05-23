Ext.define('X.store.SendTaskStore', {
    extend: 'X.util.Store',

    model: 'X.model.SendTaskModel',
    url: function (cfg) {
        var month = cfg.month ? cfg.month : 0;
        return 'sms/task-list-' + month + '/';
    }
});