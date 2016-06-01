Ext.define('X.view.SI_ContractList', {
    extend: 'X.util.List',

    title: 'SI合同管理',
    model_name: 'X.model.SI_ContractModel',
    store_name: 'X.store.SI_ContractStore',
    button_list: [{
        text: '增加', type: 'insert',
        action: 'X.view.SI_ContractEditWindow'
    }, {
        text: '修改', type: 'update',
        action: 'X.view.SI_ContractEditWindow'
    }, {
        text: '报帐清单', type: 'function',
        action: function (grid, record) {
            var stat = "all";
            var contract = record.get("id");
            var name = record.get("no") + record.get("name");
            tools.addTab(Ext.getCmp('MainFrame'), '{"cls":"X.view.SI_PayList","cfg":{"stat": "' + stat + '", "contract": "' + contract + '"}}', '报账清单#' + name);
        }
    }, {
        text: '下载协议', type: 'function',
        action: function (grid, record) {
            Ext.Msg.alert('下载协议', '<a href="extra/si-contract-download/' + record.get('id') + '/">' + record.get("no") + record.get("name") + '</a>');
        }
    }]
});