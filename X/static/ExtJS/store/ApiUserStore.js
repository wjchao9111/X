Ext.define('X.store.ApiUserStore', {
    extend: 'X.util.Store',

    model: 'X.model.UserModel',
    url: 'sms/api-user-list/'
});