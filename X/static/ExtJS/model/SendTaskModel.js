Ext.define('X.model.SendTaskModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {
            name: 'type', label: '类型', field: 'combo', choice: 'send.type', value: 'default', field_cfg: {
            listeners: {
                select: function (combo, record, opts) {
                    if (record[0].get("id") == 'dynamic') {
                        Ext.Msg.show({
                            title: "使用说明",
                            msg: "<img src='static/img/dynamic.png'>",
                            minWidth: 936,
                            minHeight: 660
                        });
                    }
                }
            }
        }
        },
        {name: 'type_display', label: '类型', show: true},
        {name: 'name', label: '名称', show: true, field: 'textfield'},
        {name: 'priority', label: '优先级', field: 'combo', value: 9, choice: 'user.priority'},
        {name: 'priority_display', label: '优先级', show: true},
        {name: 'phones', label: '手机号', field: 'textfield', regex: re_phones, blank: true},
        {name: 'groups', label: '通讯录组', field: 'hiddenfield'},
        {name: 'groups-display', label: '通讯录组', field: 'displayfield'},
        {name: 'file', label: '号码文件', field: 'filefield', blank: true},
        {name: 'content', label: '内容', show: true, field: 'textareafield', field_cfg: {height: 80}},
        {name: 'init', label: '创建时间', show: true},
        {name: 'stat', label: '状态'},
        {name: 'stat_display', label: '状态', show: true},
        {name: 'pause', label: '暂停'},
        {
            name: 'timing-date', type: 'date', format: 'Y-m-d', label: '开始-日期', field: 'datefield', blank: true,
            field_cfg: {format: 'Y-m-d'}
        },
        {
            name: 'timing-time', type: 'date', format: 'HH:i:s', label: '开始-时间', field: 'timefield', blank: true,
            field_cfg: {format: 'H:i:s'}
        },
        {name: 'timing', label: '开始时间', show: true},
        {name: 'ending-date', type: 'date', format: 'Y-m-d', label: '结束-日期'},
        {name: 'ending-time', type: 'time', format: 'HH:i:s', label: '结束-时间'},
        {name: 'ending', label: '结束时间'},
        {name: 'count', label: '短信数量', show: true},
        {name: 'submit', label: '已提交', show: true},
        {name: 'success', label: '已成功', show: true},
        {name: 'error', label: '已失败', show: true},
        {name: 'user_id', label: '用户'},
        {name: 'user', label: '用户', show: true}
    ]
});