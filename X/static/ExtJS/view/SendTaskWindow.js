Ext.define('X.view.SendTaskWindow', {
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
});