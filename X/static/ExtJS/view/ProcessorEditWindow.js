Ext.define('X.view.ProcessorEditWindow', {
    extend: 'X.util.Window',

    height: 190,
    width: 400,
    base_title: '进程',
    base_url: 'sms/processor-{0}/',
    model_name: 'X.model.ProcessorModel'
});