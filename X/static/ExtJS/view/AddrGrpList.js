Ext.define('X.view.AddrGrpList', {
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
});