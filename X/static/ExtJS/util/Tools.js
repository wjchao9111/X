Ext.define('X.util.Tools', {
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
});