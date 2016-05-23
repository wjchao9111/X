Ext.define('X.view.MsgChart', {
    extend: 'X.util.Chart',

    x_title: '每小时短信发送量',
    y_title: '短信数量',
    x_fields: ['hour'],
    y_fields: ['count'],
    store: 'X.store.MsgChartStore'
});