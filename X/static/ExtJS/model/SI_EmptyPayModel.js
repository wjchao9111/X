Ext.define('X.model.SI_EmptyPayModel', {
    extend: 'Ext.data.Model', fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'pay_no', label: '报账单号', show: true, field: 'textfield', blank: true, regex: /^\d{16}(,\d+)*$/},
        {name: 'user', label: '操作员', show: true}]
});