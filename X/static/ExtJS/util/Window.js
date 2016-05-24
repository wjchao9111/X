Ext.define('X.util.Window', {
    extend: 'Ext.window.Window',

    timeout: 10000,
    waitmsg: '正在提交，请稍等！',
    url: null,
    layout: 'fit',
    button_list: [],
    default_buttons: [{
        xtype: 'button',
        text: '确定', handler: function (btn) {
            this.findParentByType('window').ok_click(btn);
        }
    }, {
        xtype: 'button',
        text: '取消', handler: function (btn) {
            this.findParentByType('window').cancel_click(btn);
        }
    }],
    constructor: function (config) {
        var me = this;
        me.cfg = config || {};
        if (me.cfg) {
            me.grid = me.cfg.grid;
            me.record = me.cfg.record;
        }
        if (me.record) {
            if (me.update_url) {
                me.url = me.update_url;
            }
            else {
                me.url = me.base_url.format('update');
            }
        }
        else {
            if (me.insert_url) {
                me.url = me.insert_url;
            }
            else {
                me.url = me.base_url.format('insert');
            }
        }
        me.callParent();
    }
    ,
    ok_click: function (btn) {
        var me = this;
        var form = btn.findParentByType('form');
        if (!form.isValid()) {
            Ext.Msg.alert("错误", "您输入的信息有误！");
            return false;
        }
        form.getForm().submit({
            url: me.url,
            method: 'POST',
            timeout: me.timeout,
            waitTitle: "提示",
            waitMsg: me.waitmsg,
            success: function (form, action) {
                try {
                    var json = Ext.decode(action.response.responseText);
                    if (me.grid) {
                        me.grid.store.reload();
                    }
                } catch (e) {
                    Ext.Msg.alert('错误', action.response.responseText);
                }
                me.close();
                Ext.Msg.alert('成功', json.message);
            },
            failure: function (form, action) {
                try {
                    var json = Ext.decode(action.response.responseText);
                    Ext.Msg.alert('错误', json.message);
                } catch (e) {
                    Ext.Msg.alert('错误', action.response.responseText);
                }
            }
        });
    }
    ,
    cancel_click: function (btn) {
        this.close();
    }
    ,
    listeners: {
        'afterrender': function () {
            var me = this;
            var record = me.record;
            if (record) {
                if (me.update_title) {
                    me.setTitle(me.update_title);
                }
                else {
                    me.setTitle('修改' + me.base_title);
                }
                var form = tools.getCmp(me, {xtype: "form"}).form;
                var field_values = {};
                var field_list = form.getFields().items;
                for (var i in field_list) {
                    var field = field_list[i];
                    var key = field.name;
                    var key = key.split('.')[1];
                    var value = me.record.data[key];
                    if (field.store && !field.store.type) {
                        var store = field.store;
                        store.remoteFilter = true;
                        store.proxy.encodeFilters = function (filters) {
                            return filters[0].value;
                        };
                        store.filter({id: 'query', property: 'query', value: value});
                    }
                    field.setValue(value);

                }
                form.setValues(field_values);
            }
            else {
                if (me.insert_title) {
                    me.setTitle(me.insert_title);
                }
                else {
                    me.setTitle('新增' + me.base_title);
                }
            }
        }
    }
    ,
    initComponent: function () {
        var me = this;
        var buttons = [];
        for (var i in me.button_list) {
            buttons.push(me.button_list[i]);
        }
        for (var i in me.default_buttons) {
            buttons.push(me.default_buttons[i]);
        }
        var inputs = [];
        var model = Ext.create(me.model_name);
        for (var i = 0; i < model.fields.length; i++) {
            var field = model.fields.getAt(i);
            if (field.field) {
                var input = {
                    xtype: field.field,
                    fieldLabel: field.label,
                    name: 'object.' + field.name,
                    allowBlank: !!field.blank,
                    blankText: '请输入' + field.label
                };
                if (field.regex) {
                    Ext.applyIf(input, {
                        regex: field.regex,
                        regexText: '您输入的' + me.base_title + '格式不正确！'
                    })
                }

                if (field.field == 'combo') {
                    Ext.applyIf(input, {
                        typeAhead: true,
                        valueField: field.id_field ? field.id_field : 'id',
                        displayField: field.display_field ? field.display_field : 'name',
                        vtype: 'comboBox',
                        vtypeText: '请在列表中选择一个选项！'
                    });
                    if (field.choice) {
                        Ext.applyIf(input, {
                            store: Ext.create('X.store.KVStore', {type: field.choice}),
                            queryMode: 'local'
                        });
                    }
                    else {
                        Ext.applyIf(input, {
                            store: Ext.create(field.store, me.cfg),
                            queryMode: 'remote',
                            triggerAction: 'query',
                            queryParam: 'query',
                            minChars: 0
                        });
                    }
                }
                if (field.regex) {
                    Ext.applyIf(input, {
                        regex: field.regex,
                        regexText: '您输入的' + me.base_title + '格式不正确！'
                    })
                }
                if (!me.record && field.value) {
                    Ext.applyIf(input, {
                        value: field.value
                    });
                }
                if (field.field_cfg) {
                    Ext.applyIf(input, field.field_cfg);
                }
                inputs.push(input);
            }
        }

        Ext.applyIf(me, {
            items: [{
                xtype: 'form',
                border: false,
                autoScroll: true,
                bodyPadding: 10,
                items: [{
                    xtype: 'fieldset',
                    title: me.base_title,
                    defaultType: 'textfield',
                    defaults: {
                        anchor: '100%',
                        allowBlank: false,
                        labelWidth: 60,
                        labelAlign: 'left',
                        idField: 'object.id'
                    },
                    items: inputs
                }],
                buttons: buttons
            }]
        });
        me.callParent(arguments);
    }
})
;