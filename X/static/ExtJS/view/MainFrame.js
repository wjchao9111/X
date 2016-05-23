Ext.define('X.view.MainFrame', {
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
	