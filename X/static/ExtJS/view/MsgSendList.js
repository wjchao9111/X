Ext.define('X.view.MsgSendList', {
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
});