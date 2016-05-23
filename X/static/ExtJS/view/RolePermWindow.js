Ext.define('X.view.RolePermWindow', {
    extend: 'Ext.window.Window',

    requires: [
        'Ext.form.Panel',
        'Ext.tree.Panel'
    ],

    height: 400,
    width: 400,
    layout: 'fit',
    title: '修改权限',

    constructor: function (config) {
        var me = this;
        me.grid = config.grid;
        me.record = config.record;
        me.callParent();
    },

    initComponent: function () {
        var me = this;

        var check_change = function (node, flag) {
            function doCheck(node, flag) {
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
            var permTree = tools.getCmp(me, {xtype: 'treepanel'});
            var records = permTree.getChecked();
            var record = me.record;
            var ids = [];
            Ext.Array.each(records, function (rec) {
                ids.push(rec.get('id'));
            });
            Ext.Ajax.request({
                url: 'base/role-perm-update/',
                params: {'role.id': record.get('id'), ids: ids.join(',')},
                method: 'POST',
                success: function (response, options) {
                    try {
                        var json = Ext.decode(response.responseText);
                        Ext.Msg.alert('成功', json.message);
                        me.close();
                    }
                    catch (e) {
                        Ext.Msg.alert('错误', response.responseText);
                    }
                },
                failure: function (response, options) {
                    try {
                        var json = Ext.decode(response.responseText);
                        Ext.Msg.alert('错误', json.message);
                    } catch (e) {
                        Ext.Msg.alert('错误', response.responseText);
                    }
                }
            });
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
                            url: 'base/role-perm/?role.id=' + me.record.get('id')
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