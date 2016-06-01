Ext.define('X.model.SI_InvoiceModel', {
    extend: 'Ext.data.Model', fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'si_name', label: '供应商名', show: true, field: 'textfield'},
        {name: 'goods', label: '货物或应税劳务、服务名称', show: true, field: 'textfield'},
        {name: 'tax_del', label: '不含税价', show: true, field: 'textfield', regex: re_number},
        {name: 'tax_rate', label: '税率', show: true, field: 'textfield', regex: re_percent},
        {name: 'tax_add', label: '含税总额', show: true, field: 'textfield', regex: re_number},
        {name: 'no', label: '增值税专用发票编号', show: true, field: 'textfield', regex: re_digital},
        {name: 'code', label: '发票代码', show: true, field: 'textfield', regex: re_digital},
        {name: 'draw_date', label: '开票日期', show: true, field: 'datefield', field_cfg: {format: 'Y-m-d'}},
        {name: 'recv_date', label: '收票日期', show: true, field: 'datefield', field_cfg: {format: 'Y-m-d'}},
        {name: 'pay_id', label: '报账单', field: 'combo', store: 'X.store.SI_PayStore'},
        {name: 'pay', label: '报账单', show: true}]
});