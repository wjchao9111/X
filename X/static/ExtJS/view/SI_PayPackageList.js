Ext.define('X.view.SI_PayPackageList', {
    extend: 'X.util.List',

    title: 'SI报帐管理',
    model_name: 'X.model.SI_PayPackageModel',
    store_name: 'X.store.SI_PayPackageStore',
    button_list: [{
        text: '报帐批次新增', type: 'insert', action: 'X.view.SI_PayPackageWindow'
    }, {
        text: '打印汇总报表', type: 'function',
        action: function (grid, record) {
            Ext.Msg.alert('打印汇总报表', '<a href="extra/si-pay-package-print/' + record.get('package') + '/min/" target="_blank">打印汇总报表</a><br><a href="extra/si-pay-package-print/' + record.get('package') + '/month/" target="_blank">打印月报表</a>');
        }
    }, {
        text: '下载报帐附件', type: 'function',
        action: function (grid, record) {
            Ext.Msg.alert('下载报帐附件', '<a href="extra/si-pay-package-download/' + record.get('package') + '/">下载报帐附件</a>');
        }
    }]
});