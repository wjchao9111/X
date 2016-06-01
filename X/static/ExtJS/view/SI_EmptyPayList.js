Ext.define('X.view.SI_EmptyPayList', {
    extend: 'X.util.List',

    title: 'SI报账单号管理',
    model_name: 'X.model.SI_EmptyPayModel',
    store_name: 'X.store.SI_EmptyPayStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.SI_EmptyPayEditWindow'},
        //{text: '修改', type: 'update', action: 'X.view.SI_EmptyPayEditWindow'},
        {text: '删除', type: 'delete', action: 'extra/si-emptypay-delete/'}]
});