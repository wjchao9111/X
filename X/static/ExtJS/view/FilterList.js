Ext.define('X.view.FilterList', {
    extend: 'X.util.List',

    title: '模板管理',
    model_name: 'X.model.FilterModel',
    store_name: 'X.store.FilterStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.FilterEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.FilterEditWindow'},
        {text: '删除', type: 'delete', action: 'filter/filter-delete/'}
    ]
});