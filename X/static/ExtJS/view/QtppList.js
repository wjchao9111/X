Ext.define('X.view.QtppList', {
    extend: 'X.util.List',

    title: 'Qtpp管理',
    model_name: 'X.model.QtppModel',
    store_name: 'X.store.QtppStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.QtppEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.QtppEditWindow'},
        {text: '删除', type: 'delete', action: 'sms/qtpp-delete/'}
    ]
});