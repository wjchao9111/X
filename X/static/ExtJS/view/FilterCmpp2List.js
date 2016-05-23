Ext.define('X.view.FilterCmpp2List', {
    extend: 'X.util.List',

    title: 'Cmpp2管理',
    model_name: 'X.model.FilterCmpp2Model',
    store_name: 'X.store.FilterCmpp2Store',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.FilterCmpp2EditWindow'},
        {text: '修改', type: 'update', action: 'X.view.FilterCmpp2EditWindow'},
        {text: '删除', type: 'delete', action: 'filter/cmpp2-delete/'}
    ]
});