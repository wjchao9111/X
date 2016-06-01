Ext.define('X.view.SI_InvoiceList', {
    extend: 'X.util.List',

    title: 'SI发票管理',
    model_name: 'X.model.SI_InvoiceModel',
    store_name: 'X.store.SI_InvoiceStore',
    button_list: [{
        text: '增加', type: 'insert',
        action: 'X.view.SI_InvoiceEditWindow'
    }, {
        text: '修改', type: 'update',
        action: 'X.view.SI_InvoiceEditWindow'
    }, {
        text: '删除', type: 'delete', action: 'extra/si-invoice-delete/'
    }]
});