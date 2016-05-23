Ext.define('X.view.MsgRecvList', {
    extend: 'X.util.List',

    title: '短信接收管理',
    model_name: 'X.model.MsgRecvModel',
    store_name: 'X.store.MsgRecvStore',
    button_list: [{
        text: '内容', type: 'function', action: function (grid, record) {
            Ext.Msg.alert('短信内容', record.get('msg_content'));
        }
    }]
});