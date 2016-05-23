Ext.define('X.util.Chart', {
    extend: 'Ext.panel.Panel',

    constructor: function (cfg) {
        var me = this;
        cfg = cfg || {};
        me.cfg = cfg;
        me.callParent();
    },

    initComponent: function () {
        var me = this;

        var store = Ext.create(me.store);
        store.addListener({
            'load': function (store, records, success, options, ex) {
                if (!success) {
                    Ext.Msg.alert('错误', http_403_error);
                }
            }
        });
        var chart = Ext.create('Ext.chart.Chart', {
            style: 'background:#fff',
            animate: true,
            store: store,
            legend: {
                position: 'bottom'
            },
            axes: [{
                type: 'Numeric',
                position: 'left',
                fields: me.y_fields,
                title: me.y_title,
                grid: {
                    odd: {
                        opacity: 1,
                        fill: '#ddd',
                        stroke: '#bbb',
                        'stroke-width': 1
                    }
                },
                minimum: 0,
                adjustMinimumByMajorUnit: 0
            }, {
                type: 'Category',
                position: 'bottom',
                fields: me.x_fields,
                title: me.x_title,
                grid: true,
                label: {
                    rotate: {
                        degrees: 0
                    }
                }
            }],
            series: [{
                type: 'area',
                highlight: true,
                tips: {
                    trackMouse: true,
                    renderer: function (storeItem, item) {
                        var hour = storeItem.get('hour') + '时';
                        var count = storeItem.get(item.storeField) + '条';
                        var title = hour + '-' + count;
                        this.setTitle(title);
                        this.setWidth(title.getWidth(12) + 10);
                    }
                },
                axis: 'left',
                xField: me.x_fields[0],
                yField: me.y_fields,
                style: {
                    opacity: 0.93
                }
            }]
        });

        Ext.applyIf(me, {
            layout: 'fit',
            tbar: [{
                text: '重新加载',
                handler: function () {
                    store.reload();
                }
            }, {
                enableToggle: true,
                pressed: true,
                text: '动画效果',
                toggleHandler: function (btn, pressed) {
                    chart.animate = pressed ? {easing: 'ease', duration: 500} : false;
                }
            }],
            items: chart
        });
        me.callParent(arguments);
    }
});