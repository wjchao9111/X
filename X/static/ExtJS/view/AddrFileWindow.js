Ext.define('X.view.AddrFileWindow', {
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
});