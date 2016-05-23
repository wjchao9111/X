Ext.define('X.store.MsgSendStore', {
    extend: 'X.util.Store',

    model: 'X.model.MsgSendModel',
    url: function (cfg) {
        var month = cfg.month ? cfg.month : 0;
        var task = cfg.task ? cfg.task : 0;
        return 'sms/msg-send-list-' + month + '/' + task + '/';
    }
});