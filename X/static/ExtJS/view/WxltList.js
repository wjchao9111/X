Ext.define('X.view.WxltList', {
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