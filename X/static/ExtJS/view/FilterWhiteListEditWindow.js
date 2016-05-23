Ext.define('X.view.FilterWhiteListEditWindow', {
    extend: 'X.util.Window',

    height: 185,
    width: 400,
    base_title: '白名单',
    base_url: 'filter/whitelist-{0}/',
    model_name: 'X.model.FilterWhiteListModel'
});