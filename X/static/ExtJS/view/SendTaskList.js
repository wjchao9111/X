Ext.define('X.view.SendTaskList', {
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
});