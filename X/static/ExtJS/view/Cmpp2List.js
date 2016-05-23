Ext.define('X.view.Cmpp2List', {
    extend: 'X.util.List',

    title: 'Cmpp2管理',
    model_name: 'X.model.Cmpp2Model',
    store_name: 'X.store.Cmpp2Store',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.Cmpp2EditWindow'},
        {text: '修改', type: 'update', action: 'X.view.Cmpp2EditWindow'},
        {text: '删除', type: 'delete', action: 'sms/cmpp2-delete/'}
    ]
});