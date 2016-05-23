Ext.define('X.view.SectionList', {
    extend: 'X.util.List',

    title: '用户管理',
    model_name: 'X.model.SectionModel',
    store_name: 'X.store.SectionStore',
    button_list: [
        {text: '增加', type: 'insert', action: 'X.view.SectionEditWindow'},
        {text: '修改', type: 'update', action: 'X.view.SectionEditWindow'},
        {text: '删除', type: 'delete', action: 'sms/section-delete/'}
    ]
});