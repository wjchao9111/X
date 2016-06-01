Ext.define('X.view.SI_PayList', {
    extend: 'X.util.List',

    title: 'SI报帐管理',
    model_name: 'X.model.SI_PayModel',
    store_name: 'X.store.SI_PayStore',
    button_list: [{
        text: '关联合同', type: 'ajax', action: '/extra/si-pay-attach/'
    }, {
        text: '发票清单', type: 'function',
        action: function (grid, record) {
            var pay = record.get("id");
            var si_name = record.get("si_name").replace('VSP', '');
            var name = record.get("si_name") + record.get("prd_name") + record.get("month");
            tools.addTab(Ext.getCmp('MainFrame'), '{"cls":"X.view.SI_InvoiceList","cfg":{"pay": "' + pay + '", "default_value_pay_id":' + pay + ', "default_value_si_name":"' + si_name + '"}}', '发票清单#' + name);
        }
    }, {
        text: '验证发票', type: 'ajax', action: '/extra/si-pay-verify/'
    }, {
        text: '打印粘贴单', type: 'function',
        action: function (grid, record) {
            window.open('/extra/si-pay-print/' + record.get('id') + '/');
        }
    }, {
        text: '稽核收票', type: 'ajax', action: '/extra/si-pay-close/'
    }]
});