Ext.define('X.util.List', {
    extend: 'Ext.grid.Panel',

    loadMask: true,
    multiSelect: true,

    //cfg: {default_value_field_name:'',enable_button:['btn1','btn2']}
    constructor: function (cfg) {
        var me = this;
        cfg = cfg || {};
        me.cfg = cfg;
        me.callParent();
    },

    initComponent: function () {
        var me = this;
        var model = Ext.create(me.model_name);
        var store = Ext.create(me.store_name, me.cfg);
        store.addListener({
            'load': function (store, records, success, options, ex) {
                if (!success) {
                    Ext.Msg.alert('错误', http_403_error);
                }
            }
        });
        var button_list = me.button_list;

        var on_click = function (btn) {
            var type = btn.type;
            var action = btn.action;
            var grid = me;
            switch (type) {
                case 'insert':
                    var cfg = {grid: me};
                    for (var key in me.cfg) {
                        if (key.startsWith('default_value_')) {
                            cfg[key] = me.cfg[key]
                        }
                    }
                    Ext.create(action, cfg).show();
                    break;
                case 'update':
                    if (!grid.getSelectionModel().getCount() >= 1) {
                        Ext.Msg.alert('提示', '没有选择任何数据!');
                        return false;
                    }
                    //var record = grid.getSelectionModel().getSelection()[0];
                    var record = grid.getStore().getAt(grid.getStore().indexOf(grid.getSelectionModel().getSelection()[0]));
                    var cfg = {grid: grid, record: record};
                    for (var key in me.cfg) {
                        if (key.startsWith('default_value_')) {
                            cfg[key] = me.cfg[key]
                        }
                    }
                    Ext.create(action, cfg).show();
                    break;
                case 'delete':
                    if (!grid.getSelectionModel().getCount() >= 1) {
                        Ext.Msg.alert('提示', '没有选择任何数据!');
                        return false;
                    }
                    Ext.Msg.confirm('请确认', '是否真的要删除数据？', function (button, text) {
                        if (button != 'yes') {
                            return false;
                        }
                        var ids = [];
                        Ext.each(grid.getSelectionModel().getSelection(), function (record) {
                            ids.push(record.get("id"));
                        });
                        Ext.Ajax.request({
                            url: action,
                            params: {ids: ids.join(',')},
                            method: 'POST',
                            success: function (response, options) {
                                try {
                                    var json = Ext.decode(response.responseText);
                                    grid.getStore().reload();
                                    Ext.Msg.alert('成功', json.message);
                                } catch (e) {
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
                    });
                    break;
                case 'ajax':
                    if (!grid.getSelectionModel().getCount() >= 1) {
                        Ext.Msg.alert('提示', '没有选择任何数据!');
                        return false;
                    }
                    //var record = grid.getSelectionModel().getSelection()[0];
                    var record = grid.getStore().getAt(grid.getStore().indexOf(grid.getSelectionModel().getSelection()[0]));
                    Ext.Ajax.request({
                        url: action + record.get("id") + '/',
                        params: {},
                        method: 'POST',
                        success: function (response, options) {
                            try {
                                var json = Ext.decode(response.responseText);
                                grid.getStore().reload();
                                Ext.Msg.alert('成功', json.message);
                            } catch (e) {
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
                    break;
                case 'function':
                    if (!grid.getSelectionModel().getCount() >= 1) {
                        Ext.Msg.alert('提示', '没有选择任何数据!');
                        return false;
                    }
                    //var record = grid.getSelectionModel().getSelection()[0];
                    var record = grid.getStore().getAt(grid.getStore().indexOf(grid.getSelectionModel().getSelection()[0]));
                    action(me, record);
                    break;
                case 'export':
                    Ext.Msg.confirm('请确认', '一次性导出大量数据，会造成系统运行缓慢，请不要频繁或重复执行导出操作，提交导出操作后系统可能会较长时间内无响应，约几分钟或更长时间之后才开始下载导出结果，是否真的要导出数据？', function (button, text) {
                        if (button != 'yes') {
                            return false;
                        }
                        window.location.href = grid.store.proxy.url + 'export/';
                    });
                    break;
                case 'report':
                    window.location.href = grid.store.proxy.url + 'report/';
                    break;
            }
        };

        var menu = [];
        for (var i in button_list) {
            if (!me.cfg.enable_button || me.cfg.enable_button.indexOf(button_list[i].text) > -1) {
                var text = button_list[i].text;
                var type = button_list[i].type;
                var action = button_list[i].action;
                menu.push({text: text, type: type, action: action, handler: on_click});
            }
        }
        var contextmenu = new Ext.menu.Menu({
            id: 'theContextMenu',
            items: menu
        });

        var columns = [];
        for (var i = 0; i < model.fields.length; i++) {
            var field = model.fields.getAt(i);
            if (field.show) {
                columns.push({header: field.label, dataIndex: field.name});
            }
        }

        Ext.applyIf(me, {
            store: store,
            dockedItems: [{
                dock: 'top',
                xtype: 'toolbar',
                items: [{
                    width: 400,
                    fieldLabel: '搜索',
                    labelWidth: 50,
                    xtype: 'searchfield',
                    store: store
                }, '->', {
                    xtype: 'splitbutton',
                    text: '操作',
                    menu: menu
                }]
            }],
            viewConfig: {
                trackOver: false,
                emptyText: '<h1 style="margin:20px">No matching results</h1>'
            },
            columns: columns,
            bbar: Ext.create('Ext.PagingToolbar', {
                store: store,
                displayInfo: true,
                displayMsg: '显示清单 {0} - {1} of {2}',
                emptyMsg: '' //'没有清单'
            }),
            listeners: {
                itemcontextmenu: function (view, record, item, index, e) {
                    e.preventDefault();
                    contextmenu.showAt(e.getXY());
                },
                itemdblclick: function (view, record, item, index, e) {
                    e.preventDefault();
                    for (var i in menu) {
                        var text = menu[i].text;
                        var type = menu[i].type;
                        var action = menu[i].action;
                        if (text == '修改' || text == '清单') {
                            on_click(menu[i]);
                            break;
                        }
                    }
                }
            }
        });
        me.callParent(arguments);
    }
});