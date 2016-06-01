Ext.define('X.model.SI_PayPackageModel', {
    extend: 'Ext.data.Model', fields: [
        {
            name: 'package',
            label: '报账批次',
            show: true,
            field: 'textfield',
            blank: true,
            value: new Date().format('yyyyMMdd')
        },
        {name: 'id__count', label: '报账单数', show: true},
        {name: 'id__max', label: '最大报账单号'}]
});