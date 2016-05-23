Ext.define('X.model.SectionModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'carrier', label: '运营商', field: 'combo',choice:'section.carrier'},
        {name: 'carrier_display', label: '运营商', show: true},
        {name: 'section', label: '号段', show: true, field: 'textfield'}
    ]
});