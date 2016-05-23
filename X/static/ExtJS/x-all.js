var kv_data='{"cmpp2.stat": [["enabled", "\u542f\u7528"], ["disabled", "\u505c\u7528"]], "perm.type": [["menu", "\u83dc\u5355"], ["ajax", "URL"]], "section.carrier": [["CM", "\u4e2d\u56fd\u79fb\u52a8"], ["CU", "\u4e2d\u56fd\u8054\u901a"], ["CT", "\u4e2d\u56fd\u7535\u4fe1"]], "user.stat": [["normal", "\u6b63\u5e38"], ["disabled", "\u7981\u7528"]], "send.type": [["default", "\u666e\u901a\u4efb\u52a1"], ["dynamic", "\u52a8\u6001\u4efb\u52a1"]], "cmpp2.ssl": [["enabled", "\u542f\u7528"], ["disabled", "\u505c\u7528"]], "filter.stat": [["new", "\u65b0\u5efa"], ["enabled", "\u542f\u7528"], ["disabled", "\u505c\u7528"]], "dept.stat": [["normal", "\u6b63\u5e38"], ["disabled", "\u7981\u7528"]], "grp.mod": [["00", "\u79c1\u4eba"], ["01", "\u5185\u90e8\u53ea\u8bfb"], ["02", "\u5185\u90e8\u8bfb\u5199"], ["11", "\u5168\u90e8\u53ea\u8bfb"], ["12", "\u5916\u90e8\u53ea\u8bfb"], ["22", "\u5b8c\u5168\u5f00\u653e"]], "send.stat": [["init", "\u5df2\u521b\u5efa"], ["pre.start", "\u5f00\u59cb\u5206\u89e3"], ["pre.end", "\u5206\u89e3\u5b8c\u6210"], ["pre.fail", "\u5206\u89e3\u5931\u8d25"], ["send.start", "\u5f00\u59cb\u53d1\u9001"], ["send.end", "\u53d1\u9001\u5b8c\u6210"], ["send.fail", "\u53d1\u9001\u5931\u8d25"], ["cancel", "\u53d6\u6d88\u53d1\u9001"]], "dept.type": [["system", "\u7cfb\u7edf"], ["company", "\u516c\u53f8"], ["dept", "\u90e8\u95e8"]], "user.priority": [[5, "\u9ad8"], [7, "\u4e2d"], [9, "\u4f4e"]], "cmpp2.msg_fmt": [[8, "UTF-16BE"], [15, "gbk"]], "role.type": [["super", "\u8d85\u7ea7\u7ba1\u7406\u5458"], ["admin", "\u7ba1\u7406\u5458"], ["user", "\u7528\u6237"]], "filtercmpp2.stat": [["enabled", "\u542f\u7528"], ["disabled", "\u505c\u7528"]], "role.stat": [["normal", "\u6b63\u5e38"], ["disabled", "\u7981\u7528"]], "proc.pid": [[0, "Processor 0"]], "addr.sex": [["male", "\u7537"], ["female", "\u5973"]], "qtpp.stat": [["enabled", "\u542f\u7528"], ["disabled", "\u505c\u7528"]], "perm.stat": [["normal", "\u6b63\u5e38"], ["disabled", "\u7981\u7528"]]}';
var http_403_error='403 Forbidden：操作被禁止！<br>可能的原因：<br>1、网络状况不佳；<br>2、您未登陆系统；<br>3、登陆会话已超时；<br>4、您正在尝试执行没有权限的操作；<br>建议的操作：<br>1、重新之前的操作；<br>2、刷新浏览器或重新登陆；<br>3、联系您的企业管理员核实操作权限；<br>你知道吗？<br>会话超时被中断怎么办，点击右上角注销链接；<br>重新登陆后可以恢复到注销前的状态；';
Ext.Ajax.timeout = 10000;
var re_phone = /^[0-9]{11}$/;
var re_email = /^(\w)+(\.\w+)*@(\w)+((\.\w{2,20}){1,3})$/;
var re_code = /^[a-zA-Z0-9_]{4,}$/;
var re_ip = /^((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))$/;
var re_port = /^(([1-9][0-9]{0,3})|([1-5][0-9]{4})|(6[0-4][0-9]{3})|(65[0-4][0-9]{2})|(655[0-2][0-9])|(6553[0-5]))|[0]$/;
var re_sp_id = /^[0-9]{6}$/;
var re_sp_pwd = /^[0-9]{6}$/;
var re_src_id = /^[0-9]{5,20}$/;
var re_ser_id = /^[a-zA-Z0-9_]{1,10}$/;
var re_version = /^[0-9]$/;
var re_speed = /^[0-9]{1,3}$/;
var re_suffix = /^[0-9]{1,4}$/;

var re_phones = /(^(([0-9]{11}|[0-9]{13}),)*([0-9]{11}|[0-9]{13})$)|(^$)/;

var qtpp_url = 'http://218.207.87.21:8080/dnmms/services/GetSIMMS?wsdl';
if (!String.prototype.format) {
    String.prototype.format = function () {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}
if (!String.prototype.getWidth) {
    String.prototype.getWidth = function (fontSize) {
        var span = document.getElementById("__getwidth");
        if (span == null) {
            span = document.createElement("span");
            span.id = "__getwidth";
            document.body.appendChild(span);
            span.style.visibility = "hidden";
            span.style.whiteSpace = "nowrap";
        }
        span.innerText = this;
        span.style.fontSize = fontSize + "px";
        span.style.fontWeight = "bold";
        span.style.fontFamily = "helvetica, arial, verdana, sans-serif";

        return span.offsetWidth;
    }
}Ext.define('X.util.Chart', {
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
});Ext.define('X.util.List', {
    extend: 'Ext.grid.Panel',

    loadMask: true,
    multiSelect: true,

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
                    Ext.create(action, {grid: me}).show();
                    break;
                case 'update':
                    if (!grid.getSelectionModel().getCount() >= 1) {
                        Ext.Msg.alert('提示', '没有选择任何数据!');
                        return false;
                    }
                    var record = grid.getSelectionModel().getSelection()[0];
                    Ext.create(action, {grid: grid, record: record}).show();
                    break;
                case 'delete':
                    if (!grid.getSelectionModel().getCount() >= 1) {
                        Ext.Msg.alert('提示', '没有选择任何数据!');
                        return false;
                    }
                    var record = grid.getSelectionModel().getSelection()[0];
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
                case 'function':
                    if (!grid.getSelectionModel().getCount() >= 1) {
                        Ext.Msg.alert('提示', '没有选择任何数据!');
                        return false;
                    }
                    var record = grid.getSelectionModel().getSelection()[0];
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
            var text = button_list[i].text;
            var type = button_list[i].type;
            var action = button_list[i].action;
            menu.push({text: text, type: type, action: action, handler: on_click});
        }
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
            })
        });
        me.callParent(arguments);
    }
});Ext.define('X.util.SearchField', {
    extend: 'Ext.form.field.Trigger',
    alias: 'widget.searchfield',
    trigger1Cls: Ext.baseCSSPrefix + 'form-clear-trigger',
    trigger2Cls: Ext.baseCSSPrefix + 'form-search-trigger',
    hasSearch: false,
    paramName: 'query',
    initComponent: function () {
        var me = this;
        me.callParent(arguments);
        me.on('specialkey', function (f, e) {
            if (e.getKey() == e.ENTER) {
                me.onTrigger2Click();
            }
        });
        me.store.remoteFilter = true;
        if (!me.store.proxy.hasOwnProperty('filterParam')) {
            me.store.proxy.filterParam = me.paramName;
        }
        me.store.proxy.encodeFilters = function (filters) {
            return filters[0].value;
        }
    },

    afterRender: function () {
        this.callParent();
        this.triggerCell.item(0).setDisplayed(false);
    },

    onTrigger1Click: function () {
        var me = this;

        if (me.hasSearch) {
            me.setValue('');
            me.store.clearFilter();
            me.hasSearch = false;
            me.triggerCell.item(0).setDisplayed(false);
            me.updateLayout();
        }
    },

    onTrigger2Click: function () {
        var me = this,
            value = me.getValue();

        if (value.length > 0) {
            me.store.filter({
                id: me.paramName,
                property: me.paramName,
                value: value
            });
            me.hasSearch = true;
            me.triggerCell.item(0).setDisplayed(true);
            me.updateLayout();
        }
    }
});Ext.define('X.util.Store', {
    extend: 'Ext.data.Store',

    model: null,
    url: null,

    constructor: function (cfg) {
        var me = this;
        cfg = cfg || {};

        var url = me.url;
        if (typeof(url) == 'function') {
            url = url(cfg);
        }

        me.callParent([Ext.apply({
            autoLoad: true,
            pageSize: 20,
            proxy: {
                type: 'ajax',
                actionMethods: {
                    create: 'POST',
                    read: 'POST',
                    update: 'POST',
                    destroy: 'POST'
                },
                url: url,
                filterParam: 'query',
                simpleSortMode: true,
                reader: {
                    type: 'json',
                    root: 'object_list',
                    totalProperty: 'object_count'
                }
            }
        }, cfg)]);
    }
});Ext.define('X.util.Tools', {
    getCmp: function (root, config) {
        var queue = [root];
        while (queue.length > 0) {
            var obj = queue.shift();
            var match = true;
            for (var name in config) {
                if (obj[name] === config[name]) continue;
                match = false;
            }
            if (match === true)return obj;
            if (obj.items != null) for (var i = 0; i < obj.items.length; i++) {
                queue.push(obj.items.items[i]);
            }
        }
    },
    getViewPort: function () {
        var viewport;
        Ext.ComponentManager.each(function (key, item) {
            if (item.xtype == 'viewport') {
                viewport = item;
            }
        });
        return viewport;
    },

    showPage: function () {
        var page = this.getViewPort();
        for (i in page.items.items) {
            var item = page.items.items[i];
            item.show();
        }
    },

    hidePage: function () {
        var page = this.getViewPort();
        for (i in page.items.items) {
            var item = page.items.items[i];
            item.hide();
        }
    },

    showWin: function () {
        Ext.ComponentManager.each(function (key, item) {
            if (item.xtype == 'window') {
                item.show();
            }
        });
    },

    hideWin: function () {
        Ext.ComponentManager.each(function (key, item) {
            if (item.xtype == 'window') {
                item.hide();
            }
        });
    },

    closeWin: function () {
        Ext.ComponentManager.each(function (key, item) {
            if (item.xtype == 'window') {
                item.close();
            }
        });
    },

    addTab: function (page, url, title) {
        if (url == '#' || url == '') return false;

        var tabPanel = this.getCmp(page, {xtype: 'tabpanel'});
        if (tabPanel == null) return false;

        var findUrl = false;
        tabPanel.items.each(function (tab) {
            if (tab.url == url) {
                tabPanel.setActiveTab(tab);
                findUrl = true;
                return false;
            }
        });
        if (findUrl) return false;

        // have not find url
        var json;
        try {
            json = Ext.decode(url);//JSON.parse(url);
        } catch (e) {
        }
        if (json) {
            if (json.cls.substr(json.cls.length - 6) == 'Window')
                Ext.create(json.cls, json.cfg).show();
            else
                var tab = tabPanel.add({
                    closable: true,
                    //iconCls: '',
                    title: title,
                    url: url,
                    layout: 'fit',
                    items: [Ext.create(json.cls, json.cfg)]
                }).show();
        }
        else {
            tabPanel.add({
                closable: true,
                //iconCls: 'cls',
                title: title,
                url: url,
                /*autoLoad : {
                 url : url,
                 scripts : true
                 }*/
                html: '<iframe id="frame1" src="' + url + '" frameborder="0" width="100%" height="100%"></iframe>'
            }).show();
        }
    },

    closeTab: function (cmp) {
        var tabs = cmp.findParentByType('tabpanel');
        var tab = cmp.findParentByType("container");
        tabs.remove(tab);
    },

    clearAll: function () {
        var page = this.getViewPort();
        tabpanel = this.getCmp(page, {xtype: 'tabpanel'});
        tabpanel.items.each(function (tab) {
            if (tab.closable) {
                tabpanel.remove(tab);
            }
        });
        this.closeWin();
    }
});Ext.apply(Ext.form.VTypes, {
    passConfirm: function (val, field) {
        if (field.confirmTo) {
            var form = field.findParentByType("form");
            var pass = form.getForm().findField(field.confirmTo);
            return (val == pass.getValue());
        }
        return true;
    },
    uniqueCode: function (val, field) {
        if (!field.uniqueKey) {
            return true;
        }
        if (!field.idField) {
            return true;
        }
        var flag = false;

        var id;//检查是否有ID
        var form = field.findParentByType("form");
        var idField = form.getForm().findField(field.idField);
        if (idField && idField.getValue()) id = idField.getValue();
        return true;
        Ext.Ajax.request({
            url: 'unique',
            async: false,
            params: {'id': id, 'type': field.uniqueKey, 'value': val},
            method: 'POST',
            success: function (response, options) {
                var json = Ext.decode(response.responseText);//JSON.parse(response.responseText);
                flag = json.unique;
            },
            failure: function (response, options) {
                flag = false;
            }
        });
        return flag;
    },
    comboBox: function (val, field) {
        return !!field.getDisplayValue();
    }
});Ext.define('X.util.Window', {
    extend: 'Ext.window.Window',

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
            url: this.url,
            method: 'POST',
            waitTitle: "提示",
            waitMsg: 'Submitting your data',
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
;Ext.define('X.model.AddrFileModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', field: 'hiddenfield'},
        {name: 'file', label: '文件', field: 'filefield'},
        {name: 'group_id', label: '组', field: 'combo', store: 'X.store.AddrGrpStore'}
    ]
});Ext.define('X.model.AddrGrpModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'name', label: '组名', show: true, field: 'textfield'},
        {name: 'user_id', label: '用户'},
        {name: 'user', label: '用户', show: true},
        {name: 'dept_id', label: '部门'},
        {name: 'dept', label: '部门', show: true},
        {name: 'mod', label: '模式', field: 'combo', choice: 'grp.mod', value: '00'},
        {name: 'mod_display', label: '模式', show: true}
    ]
});Ext.define('X.model.AddrModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'phone', label: '手机', show: true, field: 'textfield', regex: re_phone},
        {name: 'name', label: '姓名', show: true, field: 'textfield'},
        {name: 'sex', label: '性别', show: true, field: 'combo', blank: true, choice: 'addr.sex'},
        {name: 'email', label: '邮箱', show: true, field: 'textfield', blank: true, regex: re_email},
        {name: 'company', label: '公司', show: true, field: 'textfield', blank: true},
        {name: 'dept', label: '部门', show: true, field: 'textfield', blank: true},
        {name: 'post', label: '邮编', show: true, field: 'textfield', blank: true},
        {name: 'addr', label: '地址', show: true, field: 'textfield', blank: true},
        {name: 'group_id', label: '组名', field: 'combo', store: 'X.store.AddrGrpStore'},
        {name: 'group', label: '组名', show: true}
    ]
});Ext.define('X.model.Cmpp2Model', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'sock_source_ip', label: '服务器IP', show: true, field: 'textfield', regex: re_ip, value: '111.11.84.'},
        {name: 'sock_source_port', label: '服务器端口', show: true, field: 'hiddenfield', regex: re_port, value: '0'},
        {name: 'sock_target_ip', label: '网关', show: true, field: 'textfield', regex: re_ip, value: '218.207.67.136'},
        {name: 'sock_target_port', label: '网关端口', show: true, field: 'textfield', regex: re_port, value: '7890'},
        {name: 'cmpp_sp_id', label: '企业代码', show: true, field: 'textfield', regex: re_sp_id},
        {name: 'cmpp_sp_pwd', label: '登陆密码', show: true, field: 'textfield', regex: re_sp_pwd, value: '123456'},
        {name: 'cmpp_src_id', label: '服务代码', show: true, field: 'textfield', regex: re_src_id},
        {name: 'cmpp_service_id', label: '业务代码', show: true, field: 'textfield', regex: re_ser_id, value: 'MHE0010501'},
        {name: 'cmpp_version_1', label: '主版本号', show: true, field: 'hiddenfield', value: '2', regex: re_version},
        {name: 'cmpp_version_2', label: '副版本号', show: true, field: 'hiddenfield', value: '0', regex: re_version},
        {name: 'cmpp_commit_speed', label: '发送速度', show: true, field: 'textfield', regex: re_speed, value: '20'},
        {name: 'cmpp_sign_zh', label: '中文签名', show: true, field: 'textfield'},
        {name: 'cmpp_sign_en', label: '英文签名', show: true, field: 'textfield'},
        {name: 'cmpp_msg_fmt', label: '短信编码', field: 'combo', choice: 'cmpp2.msg_fmt', value: 8},
        {name: 'cmpp_msg_fmt_display', label: '短信编码', show: true},
        {name: 'cmpp_status', label: '端口状态', field: 'combo', choice: 'cmpp2.stat', value: 'enabled'},
        {name: 'cmpp_status_display', label: '端口状态', show: true},
        {name: 'cmpp_ssl', label: '启用SSL', field: 'combo', choice: 'cmpp2.ssl', value: 'disabled'},
        {name: 'cmpp_ssl_display', label: '启用SSL', show: true},
        {name: 'cmpp_dept_id', label: '归属部门', field: 'combo', store: 'X.store.DeptStore'},
        {name: 'cmpp_dept', label: '归属部门', show: true}
    ]
});Ext.define('X.model.DeptModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'name', label: '名称', show: true, field: 'textfield'},
        {name: 'stat', label: '状态', field: 'combo', value: 'normal', choice: 'dept.stat'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'type', label: '类型'},
        {name: 'type_display', label: '类型', show: true},
        {name: 'parent_id', label: '归属', field: 'combo', store: 'X.store.DeptStore', blank: true},
        {name: 'parent', label: '归属', show: true}
    ]
});Ext.define('X.model.FilterAuditModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'name', label: '名称', show: true, field: 'textfield'},
        {name: 'text', label: '内容', show: true, field: 'textareafield', field_cfg: {height: 80}},
        {name: 'note', label: '审核意见', show: true, field: 'textfield'},
        {name: 'regex', label: '正则表达式', field: 'textareafield', field_cfg: {height: 80}},
        {name: 'cmpp_cfg', label: '归属端口', show: true},
        {name: 'stat', label: '状态', field: 'combo', choice: 'filter.stat'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'user', label: '归属用户', show: true}
    ]
});Ext.define('X.model.FilterCmpp2Model', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'sock_source_ip', label: '服务器IP', show: true, field: 'textfield', regex: re_ip, value: '111.11.84.'},
        {name: 'sock_source_port', label: '服务器端口', show: true, field: 'hiddenfield', regex: re_port, value: '0'},
        {name: 'sock_target_ip', label: '网关', show: true, field: 'textfield', regex: re_ip, value: '218.207.67.136'},
        {name: 'sock_target_port', label: '网关端口', show: true, field: 'textfield', regex: re_port, value: '7890'},
        {name: 'sock_accept_ip', label: '客户端IP地址', show: true, field: 'textfield', regex: re_ip},
        {name: 'cmpp_sp_id', label: '企业代码', show: true, field: 'textfield', regex: re_sp_id},
        {name: 'cmpp_src_id', label: '服务代码', show: true, field: 'textfield', regex: re_src_id},
        {name: 'cmpp_status', label: '端口状态', field: 'combo', choice: 'filtercmpp2.stat', value: 'enabled'},
        {name: 'cmpp_status_display', label: '端口状态', show: true},
        {name: 'cmpp_dept_id', label: '归属部门', field: 'combo', store: 'X.store.DeptStore'},
        {name: 'cmpp_dept', label: '归属部门', show: true}
    ]
});Ext.define('X.model.FilterModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'name', label: '名称', show: true, field: 'textfield'},
        {name: 'text', label: '内容', show: true, field: 'textareafield', field_cfg: {height: 80}},
        {name: 'note', label: '审核意见', show: true, field: 'displayfield'},
        {name: 'regex', label: '正则表达式'},
        {name: 'cmpp_cfg', label: '归属端口', show: true},
        {name: 'stat', label: '状态'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'user', label: '归属用户', show: true}
    ]
});Ext.define('X.model.FilterWhiteListModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'src_id', label: '服务代码', show: true, field: 'textfield', regex: re_src_id},
        {name: 'name', label: '名称', show: true, field: 'textfield'}
    ]
});Ext.define('X.model.HourChartModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'hour'},
        {name: 'count'}
    ]
});Ext.define('X.model.KVModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编码'},
        {name: 'name', label: '名称'}
    ]
});Ext.define('X.model.MsgRecvModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true},
        {name: 'dest_id', label: '端口号', show: true},
        {name: 'src_terminal_id', label: '手机号码', show: true},
        {name: 'msg_content', label: '信息内容', show: true},
        {name: 'msg_recv_time', label: '接收时间', show: true}
    ]
});Ext.define('X.model.MsgSendModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true},
        {name: 'dest_terminal_id', label: '发送号码', show: true},
        {name: 'src_id', label: '扩展码', show: true},
        {name: 'msg_content', label: '信息内容', show: true},
        {name: 'msg_count', label: '拆分条数', show: true},
        {name: 'msg_stat', label: '发送状态'},
        {name: 'msg_stat_display', label: '发送状态', show: true},
        {name: 'msg_init_time', label: '创建时间', show: true},
        {name: 'msg_send_time', label: '发送时间', show: true},
        {name: 'msg_ack_time', label: '回执时间', show: true},
        {name: 'msg_ack_result', label: '回执内容', show: true},
        {name: 'msg_feed_time', label: '状态报告时间', show: true},
        {name: 'msg_feed_result', label: '状态报告内容', show: true},
        {name: 'registered_delivery', label: '是否获取短信状态报告', show: true},
        {name: 'valid_time', label: '有效时间', show: true},
        {name: 'at_time', label: '定时下发时间', show: true},
        {name: 'msg_user', label: '用户', show: true},
        {name: 'msg_task', label: '任务'}
    ]
});Ext.define('X.model.PermModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'code', label: '编码', show: true, field: 'textfield'},
        {name: 'name', label: '名称', show: true, field: 'textfield'},
        {name: 'value', label: '资源', show: true, field: 'textfield'},
        {name: 'stat', label: '状态', field: 'combo', choice: 'perm.stat', value: 'normal'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'type', label: '类型', field: 'combo', choice: 'perm.type'},
        {name: 'type_display', label: '类型', show: true},
        {name: 'note', label: '备注', show: true, field: 'textfield'},
        {name: 'parent_id', label: '归属', field: 'combo', blank: true, store: 'X.store.PermStore'},
        {name: 'parent', label: '归属', show: true}
    ]
});Ext.define('X.model.ProcessorModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', field: 'hiddenfield'},
        {name: 'dept_id', label: '企业', field: 'combo', store: 'X.store.DeptStore'},
        {name: 'pid', label: '进程编号', field: 'combo', choice: 'proc.pid'}
    ]
});Ext.define('X.model.QtppModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'qtpp_wsdl_url', label: 'wsdl地址', show: true, field: 'textfield', value: qtpp_url},
        {name: 'qtpp_si_code', label: 'SI标识', show: true, field: 'textfield'},
        {name: 'qtpp_service_code', label: '业务代码', show: true, field: 'textfield'},
        {name: 'qtpp_ec_code', label: '集团编码', show: true, field: 'textfield'},
        {name: 'qtpp_fun_code', label: '功能点', show: true, field: 'textfield', blank: true},
        {name: 'qtpp_ser_code', label: '服务代码', show: true, field: 'textfield', blank: true},
        {name: 'qtpp_src_id', label: '源号码', show: true, field: 'textfield', blank: true},
        {name: 'qtpp_status', label: '端口状态',  field: 'combo', choice: 'qtpp.stat', value: 'enabled'},
        {name: 'qtpp_status_display', label: '端口状态', show: true},
        {name: 'qtpp_dept_id', label: '归属部门', field: 'combo', store: 'X.store.DeptStore'},
        {name: 'qtpp_dept', label: '归属部门', show: true}]
});Ext.define('X.model.RoleModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'name', label: '名称', show: true, field: 'textfield'},
        {name: 'type', label: '类型'},
        {name: 'type_display', label: '类型', show: true},
        {name: 'stat', label: '状态', field: 'combo', choice: 'role.stat', value: 'normal'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'dept_id', label: '归属'},
        {name: 'dept', label: '归属', show: true}
    ]
});Ext.define('X.model.SectionModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'carrier', label: '运营商', field: 'combo',choice:'section.carrier'},
        {name: 'carrier_display', label: '运营商', show: true},
        {name: 'section', label: '号段', show: true, field: 'textfield'}
    ]
});Ext.define('X.model.SendTaskModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {
            name: 'type', label: '类型', field: 'combo', choice: 'send.type', value: 'default', field_cfg: {
            listeners: {
                select: function (combo, record, opts) {
                    if (record[0].get("id") == 'dynamic') {
                        Ext.Msg.show({
                            title: "使用说明",
                            msg: "<img src='static/img/dynamic.png'>",
                            minWidth: 936,
                            minHeight: 660
                        });
                    }
                }
            }
        }
        },
        {name: 'type_display', label: '类型', show: true},
        {name: 'name', label: '名称', show: true, field: 'textfield'},
        {name: 'priority', label: '优先级', field: 'combo', value: 9, choice: 'user.priority'},
        {name: 'priority_display', label: '优先级', show: true},
        {name: 'phones', label: '手机号', field: 'textfield', regex: re_phones, blank: true},
        {name: 'groups', label: '通讯录组', field: 'hiddenfield'},
        {name: 'groups-display', label: '通讯录组', field: 'displayfield'},
        {name: 'file', label: '号码文件', field: 'filefield', blank: true},
        {name: 'content', label: '内容', show: true, field: 'textareafield', field_cfg: {height: 80}},
        {name: 'init', label: '创建时间', show: true},
        {name: 'stat', label: '状态'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'pause', label: '暂停'},
        {
            name: 'timing-date', type: 'date', format: 'Y-m-d', label: '开始-日期', field: 'datefield', blank: true,
            field_cfg: {format: 'Y-m-d'}
        },
        {
            name: 'timing-time', type: 'date', format: 'HH:i:s', label: '开始-时间', field: 'timefield', blank: true,
            field_cfg: {format: 'H:i:s'}
        },
        {name: 'timing', label: '开始时间', show: true},
        {name: 'ending-date', type: 'date', format: 'Y-m-d', label: '结束-日期'},
        {name: 'ending-time', type: 'time', format: 'HH:i:s', label: '结束-时间'},
        {name: 'ending', label: '结束时间'},
        {name: 'count', label: '短信数量', show: true},
        {name: 'submit', label: '已提交', show: true},
        {name: 'success', label: '已成功', show: true},
        {name: 'error', label: '已失败', show: true},
        {name: 'user_id', label: '用户'},
        {name: 'user', label: '用户', show: true}
    ]
});Ext.define('X.model.SuModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'combo', store: 'X.store.UserStore'}
    ]
});Ext.define('X.model.UserModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'code', label: '账号', show: true, field: 'textfield', regex: re_code},
        {name: 'pwd', label: '密码', field: 'textfield', blank: true, field_cfg: {inputType: 'password'}},
        {
            name: 'pwd_confirm', label: '确认', field: 'textfield', blank: true,
            field_cfg: {inputType: 'password', vtype: 'passConfirm', confirmTo: 'object.pwd', vtypeText: '两次输入密码不一致！'}
        },
        {name: 'name', label: '姓名', show: true, field: 'textfield'},
        {name: 'phone', label: '手机', show: true, field: 'textfield', regex: re_phone},
        {name: 'email', label: '邮箱', show: true, field: 'textfield', regex: re_email},
        {name: 'suffix', label: '扩展码', show: true, field: 'textfield', blank: true, regex: re_suffix},
        {name: 'priority', label: '优先级', field: 'combo', choice: 'user.priority'},
        {name: 'priority_display', label: '优先级', show: true},
        {name: 'stat', label: '状态', field: 'combo', choice: 'user.stat',value:'normal'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'dept_id', label: '归属', field: 'combo', store: 'X.store.DeptStore'},
        {name: 'role_id', label: '角色', field: 'combo', store: 'X.store.RoleStore'},
        {name: 'dept', label: '归属', show: true},
        {name: 'role', label: '角色', show: true}
    ]
});Ext.define('X.model.UserResetPassModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'code', label: '账号', show: true, field: 'hiddenfield'},
        {name: 'old_pwd', label: '旧密码', field: 'textfield', field_cfg: {inputType: 'password'}},
        {name: 'pwd', label: '新密码', field: 'textfield', field_cfg: {inputType: 'password'}},
        {
            name: 'pwd_confirm', label: '确认', field: 'textfield',
            field_cfg: {inputType: 'password', vtype: 'passConfirm', confirmTo: 'object.pwd', vtypeText: '两次输入密码不一致！'}
        }
    ]
});Ext.define('X.model.WxltModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'pinid', label: 'pinid', show: true, field: 'textfield'},
        {name: 'accountid', label: '账号', show: true, field: 'textfield'},
        {name: 'accountpwd', label: '密码', show: true, field: 'textfield'},
        {name: 'des_key', label: '密钥', show: true, field: 'textfield'},
        {name: 'dept_user_id', label: '用户', field: 'combo', store: 'X.store.WxltUserStore'},
        {name: 'dept_user', label: '用户', show: true}
    ]
});Ext.define('X.store.AddrGrpStore', {
    extend: 'X.util.Store',

    model: 'X.model.AddrGrpModel',
    url: 'addr/grp-list/'
});Ext.define('X.store.AddrStore', {
    extend: 'X.util.Store',

    model: 'X.model.AddrModel',
    url: function (cfg) {
        var grp_id = cfg.grp_id ? cfg.grp_id : 0;
        return 'addr/addr-list/' + grp_id + '/';
    }
});Ext.define('X.store.ApiUserStore', {
    extend: 'X.util.Store',

    model: 'X.model.UserModel',
    url: 'sms/api-user-list/'
});Ext.define('X.store.Cmpp2Store', {
    extend: 'X.util.Store',

    model: 'X.model.Cmpp2Model',
    url: 'sms/cmpp2-list/'
});Ext.define('X.store.DeptStore', {
    extend: 'X.util.Store',

    model: 'X.model.DeptModel',
    url: 'base/dept-list/'
});Ext.define('X.store.FilterCmpp2Store', {
    extend: 'X.util.Store',

    model: 'X.model.FilterCmpp2Model',
    url: 'filter/cmpp2-list/'
});Ext.define('X.store.FilterStore', {
    extend: 'X.util.Store',

    model: 'X.model.FilterModel',
    url: function (cfg) {
        var stat = cfg.stat ? cfg.stat : 'all';
        return 'filter/filter-list/' + stat + '/';
    }
});Ext.define('X.store.FilterWhiteListStore', {
    extend: 'X.util.Store',

    model: 'X.model.FilterWhiteListModel',
    url: 'filter/whitelist-list/'
});Ext.define('X.store.KVStore', {
    extend: 'Ext.data.Store',
    constructor: function (cfg) {
        var me = this;
        cfg = cfg || {};
        me.type = cfg.type;
        me.data = Ext.decode(kv_data)[me.type];
        me.callParent([Ext.apply({
            data: me.data,
            model: 'X.model.KVModel'
        }, cfg)]);
    }
});Ext.define('X.store.MsgChartStore', {
    extend: 'X.util.Store',

    model: 'X.model.HourChartModel',
    url: 'sms/msg-send-count/'
});Ext.define('X.store.MsgRecvStore', {
    extend: 'X.util.Store',

    model: 'X.model.MsgRecvModel',
    url: 'sms/msg-recv-list/'
});Ext.define('X.store.MsgSendStore', {
    extend: 'X.util.Store',

    model: 'X.model.MsgSendModel',
    url: function (cfg) {
        var month = cfg.month ? cfg.month : 0;
        var task = cfg.task ? cfg.task : 0;
        return 'sms/msg-send-list-' + month + '/' + task + '/';
    }
});Ext.define('X.store.PermStore', {
    extend: 'X.util.Store',

    model: 'X.model.PermModel',
    url: 'base/perm-list/'
});Ext.define('X.store.ProcessorStore', {
    extend: 'X.util.Store',

    model: 'X.model.DeptModel',
    url: function (cfg) {
        var pid = cfg.pid >= 0 ? cfg.pid : -1;
        return pid >= 0 ? 'sms/processor-list-' + pid + '/' : 'sms/processor-list/';
    }
});Ext.define('X.store.QtppStore', {
    extend: 'X.util.Store',

    model: 'X.model.QtppModel',
    url: 'sms/qtpp-list/'
});Ext.define('X.store.RoleStore', {
    extend: 'X.util.Store',

    model: 'X.model.RoleModel',
    url: 'base/role-list/'
});Ext.define('X.store.SectionStore', {
    extend: 'X.util.Store',

    model: 'X.model.SectionModel',
    url: 'sms/section-list/'
});Ext.define('X.store.SendTaskStore', {
    extend: 'X.util.Store',

    model: 'X.model.SendTaskModel',
    url: function (cfg) {
        var month = cfg.month ? cfg.month : 0;
        return 'sms/task-list-' + month + '/';
    }
});Ext.define('X.store.UserStore', {
    extend: 'X.util.Store',

    model: 'X.model.UserModel',
    url: 'base/user-list/'
});Ext.define('X.store.WxltStore', {
    extend: 'X.util.Store',

    model: 'X.model.WxltModel',
    url: 'sms/wxlt-list/'
});Ext.define('X.store.WxltUserStore', {
    extend: 'X.util.Store',

    model: 'X.model.UserModel',
    url: 'sms/wxlt-user-list/'
});Ext.define('X.view.AddrEditWindow', {
    extend: 'X.util.Window',

    height: 390,
    width: 400,
    base_title: '联系人',
    base_url: 'addr/addr-{0}/',
    model_name: 'X.model.AddrModel'
});Ext.define('X.view.AddrFileWindow', {
    extend: 'X.util.Window',

    height: 190,
    width: 400,
    base_title: '批量',
    insert_title: '批量新增联系人',
    insert_url: 'addr/addr-file/',
    model_name: 'X.model.AddrFileModel',
    button_list: [{
        xtype: 'button',
        text: '下载模板',
        handler: function () {
            window.location.href = 'static/AddrList.xlsx'
        }
    }]
});Ext.define('X.view.AddrGrpEditWindow', {
    extend: 'X.util.Window',

    height: 190,
    width: 400,
    base_title: '组',
    base_url: 'addr/grp-{0}/',
    model_name: 'X.model.AddrGrpModel'
});Ext.define('X.view.AddrGrpList', {
    extend: 'X.util.List',

    title: '组管理',
    model_name: 'X.model.AddrGrpModel',
    store_name: 'X.store.AddrGrpStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.AddrGrpEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.AddrGrpEditWindow'},
        {text: '删除', type: 'delete', action: 'addr/grp-delete/'}, {
            text: '清单', type: 'function',
            action: function (grid, record) {
                var grp_id = record.get("id");
                var name = record.get("name");
                tools.addTab(Ext.getCmp('MainFrame'), '{"cls":"X.view.AddrList","cfg":{"grp_id": "' + grp_id + '"}}', '通讯录清单#' + name);
            }
        }
    ]
});Ext.define('X.view.AddrList', {
    extend: 'X.util.List',

    title: '联系人管理',
    model_name: 'X.model.AddrModel',
    store_name: 'X.store.AddrStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.AddrEditWindow'},
        {text: '批量增加', type: 'insert', action: 'X.view.AddrFileWindow'},
        {text: '修改', type: 'update', action: 'X.view.AddrEditWindow'},
        {text: '删除', type: 'delete', action: 'addr/addr-delete/'},
        {text: '导出', type: 'export'}
    ]
});Ext.define('X.view.ApiUserList', {
    extend: 'X.util.List',

    title: '接口用户管理',
    model_name: 'X.model.UserModel',
    store_name: 'X.store.ApiUserStore',
    button_list: []
});Ext.define('X.view.Cmpp2EditWindow', {
    extend: 'X.util.Window',

    height: 550,
    width: 400,
    base_title: 'Cmpp2',
    base_url: 'sms/cmpp2-{0}/',
    model_name: 'X.model.Cmpp2Model'
});Ext.define('X.view.Cmpp2List', {
    extend: 'X.util.List',

    title: 'Cmpp2管理',
    model_name: 'X.model.Cmpp2Model',
    store_name: 'X.store.Cmpp2Store',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.Cmpp2EditWindow'},
        {text: '修改', type: 'update', action: 'X.view.Cmpp2EditWindow'},
        {text: '删除', type: 'delete', action: 'sms/cmpp2-delete/'}
    ]
});Ext.define('X.view.DeptEditWindow', {
    extend: 'X.util.Window',

    height: 220,
    width: 400,
    base_title: '部门',
    base_url: 'base/dept-{0}/',
    model_name: 'X.model.DeptModel'
});Ext.define('X.view.DeptList', {
    extend: 'X.util.List',

    title: '部门管理',
    model_name: 'X.model.DeptModel',
    store_name: 'X.store.DeptStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.DeptEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.DeptEditWindow'},
        {text: '删除', type: 'delete', action: 'base/dept-delete/'}
    ]
});Ext.define('X.view.FilterAuditList', {
    extend: 'X.util.List',

    title: '模板管理',
    model_name: 'X.model.FilterModel',
    store_name: 'X.store.FilterStore',
    button_list: [
        {text: '审批', type: 'update', action: 'X.view.FilterAuditWindow'}
    ]
});Ext.define('X.view.FilterAuditWindow', {
    extend: 'X.util.Window',

    height: 385,
    width: 400,
    base_title: '模板',
    update_title: '审核模板',
    base_url: 'filter/filter-{0}/',
    update_url: 'filter/filter-audit/',
    model_name: 'X.model.FilterAuditModel'
});Ext.define('X.view.FilterCmpp2EditWindow', {
    extend: 'X.util.Window',

    height: 375,
    width: 400,
    base_title: 'Cmpp2',
    base_url: 'filter/cmpp2-{0}/',
    model_name: 'X.model.FilterCmpp2Model'
});Ext.define('X.view.FilterCmpp2List', {
    extend: 'X.util.List',

    title: 'Cmpp2管理',
    model_name: 'X.model.FilterCmpp2Model',
    store_name: 'X.store.FilterCmpp2Store',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.FilterCmpp2EditWindow'},
        {text: '修改', type: 'update', action: 'X.view.FilterCmpp2EditWindow'},
        {text: '删除', type: 'delete', action: 'filter/cmpp2-delete/'}
    ]
});Ext.define('X.view.FilterEditWindow', {
    extend: 'X.util.Window',

    height: 270,
    width: 400,
    base_title: '模板',
    base_url: 'filter/filter-{0}/',
    model_name: 'X.model.FilterModel'
});Ext.define('X.view.FilterList', {
    extend: 'X.util.List',

    title: '模板管理',
    model_name: 'X.model.FilterModel',
    store_name: 'X.store.FilterStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.FilterEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.FilterEditWindow'},
        {text: '删除', type: 'delete', action: 'filter/filter-delete/'}
    ]
});Ext.define('X.view.FilterWhiteListEditWindow', {
    extend: 'X.util.Window',

    height: 185,
    width: 400,
    base_title: '白名单',
    base_url: 'filter/whitelist-{0}/',
    model_name: 'X.model.FilterWhiteListModel'
});Ext.define('X.view.FilterWhiteListList', {
    extend: 'X.util.List',

    title: '白名单管理',
    model_name: 'X.model.FilterWhiteListModel',
    store_name: 'X.store.FilterWhiteListStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.FilterWhiteListEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.FilterWhiteListEditWindow'},
        {text: '删除', type: 'delete', action: 'filter/whitelist-delete/'}
    ]
});Ext.define('X.view.LoginWindow', {
    extend: 'Ext.window.Window',

    requires: ['Ext.form.Panel', 'Ext.form.FieldSet', 'Ext.form.field.Text',
        'Ext.button.Button'],

    height: 220,
    width: 400,
    title: '登陆窗口',

    constructor: function (cfg) {
        var me = this;
        cfg = cfg || {};
        me.cfg = cfg;
        me.callParent();
    },

    initComponent: function () {
        var me = this;

        var do_reset = function (btn) {
            if (enable_email(btn)) {
                return
            }
            tools.getCmp(me, {
                xtype: "form"
            }).getForm().reset();
        };

        var wait_interval = function (btn, text, sleep_time) {
            if (sleep_time <= 0) {
                btn.setText(text);
                btn.enable();
            }
            else {
                btn.setText(text + '(' + sleep_time + ')');
            }
        };

        var set_wait = function (btn, wait_time) {
            if (!btn) return false;
            btn.disable();
            var text = btn.text;
            var interval = setInterval(function () {
                wait_interval(btn, text, --wait_time);
            }, 1000);
            setTimeout(function () {
                window.clearInterval(interval);
            }, 1000 * (wait_time + 1));
        };

        var verify = function (btn, method) {
            tools.getCmp(me, {
                xtype: "form"
            }).getForm().submit({
                url: 'base/user-verify-' + method + '/',
                method: 'POST',
                waitTitle: '提示',
                waitMsg: '正在获取验证码',
                success: function (form, action) {
                    try {
                        var json = Ext.decode(action.response.responseText);
                        Ext.Msg.alert('成功', json.message);
                    } catch (e) {
                        Ext.Msg.alert('错误', action.response.responseText);
                    }
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
            set_wait(btn, 10);
        };

        var email_click_times = 0;
        var enable_email = function (btn) {
            email_click_times++;
            if (email_click_times > 10) {
                verify(btn, 'email');
                return true;
            }
        };

        var do_post = function (btn) {
            tools.getCmp(me, {
                xtype: "form"
            }).getForm().submit({
                url: 'base/user-login/',
                method: 'POST',
                waitTitle: '提示',
                waitMsg: '正在登陆系统',
                success: function (form, action) {
                    Ext.Msg.alert('成功', '登陆成功！', function (button, text) {
                        me.cfg.success();
                        me.close();
                    });
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
            set_wait(btn, 10);
        };

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'form',
                    bodyPadding: 10,
                    items: [
                        {
                            xtype: 'fieldset',
                            title: '请填写账号和密码',
                            items: [
                                {
                                    xtype: 'textfield',
                                    anchor: '100%',
                                    fieldLabel: '账号',
                                    name: 'object.code'
                                },
                                {
                                    xtype: 'textfield',
                                    anchor: '100%',
                                    fieldLabel: '密码',
                                    name: 'object.pwd',
                                    inputType: 'password'
                                }, {
                                    xtype: 'textfield',
                                    anchor: '100%',
                                    fieldLabel: '验证码',
                                    name: 'object.verify',
                                    listeners: {
                                        specialkey: function (f, e) {
                                            if (e.getKey() == e.ENTER) {
                                                do_post();
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    xtype: 'button',
                    margin: '0 5 0 10',
                    text: '获取验证码',
                    listeners: {
                        'click': function (btn) {
                            verify(btn, 'sms')
                        }
                    }
                },
                {
                    xtype: 'button',
                    margin: '0 5 0 10',
                    text: '登陆',
                    listeners: {
                        'click': do_post
                    }
                },
                {
                    xtype: 'button',
                    margin: '0 10 0 5',
                    text: '重置',
                    listeners: {
                        'click': do_reset
                    }
                }
            ]
        });

        me.callParent(arguments);
    }
});Ext.define('X.view.MainFrame', {
    extend: 'Ext.container.Viewport',

    layout: 'border',

    initComponent: function () {
        var me = this;

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'container',
                    region: 'north',
                    height: 32,
                    layout: {
                        type: 'hbox',
                        align: 'middle'
                    },
                    items: [
                        {
                            xtype: 'component',
                            flex: 1,
                            html: '<p style="font-size:16px;font-weight:bold;">X SYSTEM</p>'
                        },
                        {
                            xtype: 'component',
                            flex: 2,
                            tag: 'tools',
                            html: '<p style="font-size:16px;font-weight:bold;" align="right">欢迎：<a  href="#" onclick="page_logout()">注销</a></p>'
                        }
                    ]
                },
                {
                    xtype: 'panel',
                    region: 'west',
                    split: true,
                    margin: '0 0 0 5',
                    maxWidth: 400,
                    minWidth: 175,
                    width: 250,
                    layout: 'fit',
                    animCollapse: true,
                    collapsible: true,
                    title: '导航菜单',
                    items: [
                        {
                            xtype: 'treepanel',
                            tag: 'permtree',
                            rootVisible: false,
                            useArrows: true,
                            store: Ext.create('Ext.data.TreeStore', {
                                proxy: {
                                    type: 'ajax',
                                    url: 'base/user-perm/'
                                },
                                fields: [
                                    {name: 'text', type: 'string'},
                                    {name: 'url', type: 'string'},
                                    {name: 'id', type: 'string'},
                                    {name: 'leaf', type: 'boolean'},
                                    {name: 'qtip', type: 'string'},
                                    {name: 'cls', type: 'string'}
                                ],
                                root: {
                                    text: 'Ext JS',
                                    id: '-1',
                                    expanded: true
                                }
                            }),
                            listeners: {
                                itemclick: function (view, record) {
                                    if (record.data.url) {
                                        tools.addTab(me, record.data.url, record.data.text);
                                    }
                                }
                            }
                        }
                    ]
                },
                {
                    xtype: 'tabpanel',
                    region: 'center',
                    activeTab: 0,
                    deferredRender: true,
                    items: [
                        {
                            xtype: 'panel',
                            closable: false,
                            html: '<strong>文档下载：</strong><br>' +
                            '<a href="static/doc/使用文档.zip">使用文档</a><br>' +
                            '<a href="static/doc/接口文档.docx">接口文档</a><br>' +
                            '<strong>老接口迁移demo：</strong><br>' +
                            '<a href="static/doc/javademo.rar">java demo</a><br>' +
                            '<a href="static/doc/csharpdemo.rar">c# demo</a><br>' +
                            '<strong>新接口开发demo：</strong><br>' +
                            '阅读接口文档即可',
                            autoScroll: true,
                            title: '欢迎使用'
                        }
                    ]
                }
            ]
        });

        me.callParent(arguments);
    }

});
	Ext.define('X.view.MsgChart', {
    extend: 'X.util.Chart',

    x_title: '每小时短信发送量',
    y_title: '短信数量',
    x_fields: ['hour'],
    y_fields: ['count'],
    store: 'X.store.MsgChartStore'
});Ext.define('X.view.MsgRecvList', {
    extend: 'X.util.List',

    title: '短信接收管理',
    model_name: 'X.model.MsgRecvModel',
    store_name: 'X.store.MsgRecvStore',
    button_list: [{
        text: '内容', type: 'function', action: function (grid, record) {
            Ext.Msg.alert('短信内容', record.get('msg_content'));
        }
    }]
});Ext.define('X.view.MsgSendList', {
    extend: 'X.util.List',

    title: '短信发送管理',
    model_name: 'X.model.MsgSendModel',
    store_name: 'X.store.MsgSendStore',
    button_list: [{
        text: '内容', type: 'function', action: function (grid, record) {
            Ext.Msg.alert('短信内容', record.get('msg_content'));
        }
    }, {
        text: '报表', type: 'report'
    }]
});Ext.define('X.view.PermEditWindow', {
    extend: 'X.util.Window',

    height: 330,
    width: 400,
    base_title: '权限',
    base_url: 'base/perm-{0}/',
    model_name: 'X.model.PermModel'
});Ext.define('X.view.PermList', {
    extend: 'X.util.List',

    title: '权限管理',
    model_name: 'X.model.PermModel',
    store_name: 'X.store.PermStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.PermEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.PermEditWindow'},
        {text: '删除', type: 'delete', action: 'base/perm-delete/'}
    ]
});Ext.define('X.view.ProcessorEditWindow', {
    extend: 'X.util.Window',

    height: 190,
    width: 400,
    base_title: '进程',
    base_url: 'sms/processor-{0}/',
    model_name: 'X.model.ProcessorModel'
});Ext.define('X.view.ProcessorList', {
    extend: 'X.util.List',

    title: '进程管理',
    model_name: 'X.model.DeptModel',
    store_name: 'X.store.ProcessorStore',
    button_list: [{
        text: '修改', type: 'function', type: 'function',
        action: function (grid, record) {
            var pid = grid.cfg.pid >= 0 ? grid.cfg.pid : "";
            var record = grid.getSelectionModel().getSelection()[0];
            record = {data: {dept_id: record.data.id, pid: pid}};
            Ext.create('X.view.ProcessorEditWindow', {grid: grid, record: record}).show();
        }
    }, {
        text: '删除', type: 'delete', action: 'sms/processor-delete/'
    }]
});Ext.define('X.view.QtppEditWindow', {
    extend: 'X.util.Window',

    height: 402,
    width: 400,
    base_title: 'Qtpp',
    base_url: 'sms/qtpp-{0}/',
    model_name: 'X.model.QtppModel'
});Ext.define('X.view.QtppList', {
    extend: 'X.util.List',

    title: 'Qtpp管理',
    model_name: 'X.model.QtppModel',
    store_name: 'X.store.QtppStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.QtppEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.QtppEditWindow'},
        {text: '删除', type: 'delete', action: 'sms/qtpp-delete/'}
    ]
});Ext.define('X.view.RoleEditWindow', {
    extend: 'X.util.Window',

    height: 190,
    width: 400,
    base_title: '角色',
    base_url: 'base/role-{0}/',
    model_name: 'X.model.RoleModel'
});Ext.define('X.view.RoleList', {
    extend: 'X.util.List',

    title: '角色管理',
    model_name: 'X.model.RoleModel',
    store_name: 'X.store.RoleStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.RoleEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.RoleEditWindow'},
        {text: '删除', type: 'delete', action: 'base/role-delete/'},
        {text: '权限', type: 'update', action: 'X.view.RolePermWindow'}
    ]
});Ext.define('X.view.RolePermWindow', {
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

});Ext.define('X.view.SectionEditWindow', {
    extend: 'X.util.Window',

    height: 190,
    width: 400,
    base_title: '号段',
    base_url: 'sms/section-{0}/',
    model_name: 'X.model.SectionModel'
});Ext.define('X.view.SectionList', {
    extend: 'X.util.List',

    title: '用户管理',
    model_name: 'X.model.SectionModel',
    store_name: 'X.store.SectionStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.SectionEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.SectionEditWindow'},
        {text: '删除', type: 'delete', action: 'sms/section-delete/'}
    ]
});Ext.define('X.view.SendGrpWindow', {
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

});Ext.define('X.view.SendTaskList', {
    extend: 'X.util.List',

    title: '发送任务管理',
    model_name: 'X.model.SendTaskModel',
    store_name: 'X.store.SendTaskStore',
    button_list: [{
        text: '清单', type: 'function',
        action: function (grid, record) {
            var month = grid.cfg.month ? grid.cfg.month : 0;
            var task = record.get("id");
            var name = record.get("name");
            tools.addTab(Ext.getCmp('MainFrame'), '{"cls":"X.view.MsgSendList","cfg":{"month": "' + month + '", "task": "' + task + '"}}', '短信发送清单#' + name);
        }
    }, {
        text: '内容', type: 'function',
        action: function (grid, record) {
            Ext.Msg.alert('短信内容', record.get('content'));
        }
    }]
});Ext.define('X.view.SendTaskWindow', {
    extend: 'X.util.Window',

    height: 450,
    width: 400,
    base_title: '发送任务',
    base_url: 'sms/task-{0}/',
    model_name: 'X.model.SendTaskModel',
    button_list: [{
        xtype: 'button',
        text: '下载模板',
        handler: function () {
            window.location.href = 'static/AddrList.xlsx'
        }
    }, {
        xtype: 'button',
        text: '选择通讯录',
        handler: function (btn) {
            Ext.create('X.view.SendGrpWindow', {form: btn.findParentByType('form')}).show();
        }
    }]
});Ext.define('X.view.SuWindow', {
    extend: 'X.util.Window',

    height: 160,
    width: 400,
    base_title: '选择用户',
    insert_title: '切换用户',
    insert_url: 'su/',
    model_name: 'X.model.SuModel'
});Ext.define('X.view.UserEditWindow', {
    extend: 'X.util.Window',

    height: 450,
    width: 400,
    base_title: '用户',
    base_url: 'base/user-{0}/',
    model_name: 'X.model.UserModel'
});Ext.define('X.view.UserList', {
    extend: 'X.util.List',

    title: '用户管理',
    model_name: 'X.model.UserModel',
    store_name: 'X.store.UserStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.UserEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.UserEditWindow'},
        {text: '删除', type: 'delete', action: 'base/user-delete/'}
    ]
});Ext.define('X.view.UserResetPassWindow', {
    extend: 'X.util.Window',

    height: 200,
    width: 400,
    base_title: '用户',
    update_title: '修改用户密码',
    update_url: 'base/user-reset-pass/',
    model_name: 'X.model.UserResetPassModel'
});Ext.define('X.view.WxltEditWindow', {
    extend: 'X.util.Window',

    height: 275,
    width: 400,
    base_title: 'WXLT接口',
    base_url: 'sms/wxlt-{0}/',
    model_name: 'X.model.WxltModel'
});Ext.define('X.view.WxltList', {
    extend: 'X.util.List',

    title: 'WXLT接口管理',
    model_name: 'X.model.WxltModel',
    store_name: 'X.store.WxltStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.WxltEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.WxltEditWindow'},
        {text: '删除', type: 'delete', action: 'sms/wxlt-delete/'}
    ]
});