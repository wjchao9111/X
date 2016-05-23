Ext.define('X.view.SectionEditWindow', {
    extend: 'X.util.Window',

    height: 190,
    width: 400,
    base_title: '号段',
    base_url: 'sms/section-{0}/',
    model_name: 'X.model.SectionModel'
});