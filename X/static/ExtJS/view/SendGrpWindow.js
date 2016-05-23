Ext.define('X.view.SendGrpWindow', {
    extend: 'Ext.window.Window',

    requires: [
        'Ext.form.Panel',
        'Ext.tree.Panel'
    ],

    height: 400,
    width: 400,
    layout: 'fit',
    title: '选择组',

    constructor: function (config) {
        var me = this;
        me.form = config.form;
        me.callParent();
    },

    initComponent: function () {
        var me = this;

        var check_change = function (node, flag) {
            function doCheck(node, flag) {
                if (!node.get("id")) return;
                node.set("checked", flag);
                if (flag) {
                    if (node.parentNode && node.parentNode.get("id") != "root") doCheck(node.parentNode, flag);
                }
                else {
                    Ext.each(node.childNodes, function (node) {
                        doCheck(node, flag);
                    });
                }
            }

            doCheck(node, flag);
        };

        var save_click = function (btn) {
            var tree = tools.getCmp(me, {xtype: 'treepanel'});
            var records = tree.getChecked();
            var record = me.record;
            var ids = [];
            Ext.Array.each(records, function (rec) {
                ids.push(rec.get('id'));
            });
            var names = [];
            Ext.Array.each(records, function (rec) {
                names.push(rec.get('text'));
            });
            var group_field = me.form.getForm().findField('object.groups');
            var display_field = me.form.getForm().findField('object.groups-display');
            group_field.setValue(ids.join(','));
            display_field.setValue(names.join(','));

            Ext.Msg.alert('成功', '已选择：' + names.join(','));
            me.close();
        };

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'treepanel',
                    rootVisible: false,
                    useArrows: true,
                    width: 250,
                    height: 300,
                    store: Ext.create('Ext.data.TreeStore', {
                        proxy: {
                            type: 'ajax',
                            url: 'addr/grp-tree/'
                        },
                        sorters: [{
                            property: 'leaf',
                            direction: 'ASC'
                        }, {
                            property: 'id',
                            direction: 'ASC'
                        }],
                        autoLoad: true,
                        autoDestroy: true
                    }),
                    listeners: {
                        checkchange: check_change
                    },
                    tbar: [{
                        text: '保存',
                        scope: this,
                        handler: save_click
                    }]
                }
            ]
        });

        me.callParent(arguments);
    }

});