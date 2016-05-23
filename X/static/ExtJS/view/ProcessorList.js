Ext.define('X.view.ProcessorList', {
    extend: 'X.util.List',

    title: '进程管理',
    model_name: 'X.model.DeptModel',
    store_name: 'X.store.ProcessorStore',
    button_list: [{
        text: '修改', type: 'function', type: 'function',
        action: function (grid, record) {
            var pid = grid.cfg.pid >= 0 ? grid.cfg.pid : "";
            var record = grid.getSelectionModel().getSelection()[0];
            record = {data: {dept_id: record.data.id, pid: pid}};
            Ext.create('X.view.ProcessorEditWindow', {grid: grid, record: record}).show();
        }
    }, {
        text: '删除', type: 'delete', action: 'sms/processor-delete/'
    }]
});