Ext.define('X.model.SI_ContractModel', {
    extend: 'Ext.data.Model', fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'si_name', label: '合作伙伴名称', show: true, field: 'textfield'},
        {name: 'prd_name', label: '业务名称', show: true, field: 'textfield'},
        {name: 'tax_rate', label: '开票税率', show: true, field: 'textfield', regex: re_percent},
        {name: 'si_share', label: '分成比例', show: true, field: 'textfield', regex: re_share},
        {name: 'si_contact', label: '联系人', show: true, field: 'textfield'},
        {name: 'si_phone', label: '联系电话', show: true, field: 'textfield', regex: re_phone},
        {name: 'no', label: '合同编号', show: true, field: 'textfield'},
        {name: 'name', label: '合同名称', show: true, field: 'textfield'},
        {name: 'sign_date', label: '签署日期', show: true, field: 'datefield', field_cfg: {format: 'Y-m-d'}},
        {name: 'eff_date', label: '合同起始日', show: true, field: 'datefield', field_cfg: {format: 'Y-m-d'}},
        {name: 'vilid_term', label: '合同年限', show: true, field: 'textfield'},
        {name: 'exp_date', label: '合同终止日', show: true, field: 'datefield', field_cfg: {format: 'Y-m-d'}},
        {name: 'delay_month', label: '延期支付月数', show: true, field: 'textfield', regex: re_digital},
        {name: 'off_date', label: '业务下线日', show: true, field: 'datefield', field_cfg: {format: 'Y-m-d'}, blank: true},
        {name: 'change_log', label: '变更记录', show: true, field: 'textfield', blank: true},
        {name: 'note', label: '备注', show: true, field: 'textfield', blank: true},
        {name: 'file', label: '合同文件', field: 'filefield'},
        {name: 'user', label: '产品经理', show: true},
        {name: 'init_time', label: '创建时间', show: true, blank: true},
        {name: 'last_time', label: '更新时间', show: true, blank: true}]
});