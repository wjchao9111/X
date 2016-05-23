Ext.define('X.store.MsgChartStore', {
    extend: 'X.util.Store',

    model: 'X.model.HourChartModel',
    url: 'sms/msg-send-count/'
});