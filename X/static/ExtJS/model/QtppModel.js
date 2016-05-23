Ext.define('X.model.QtppModel', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', label: '编号', show: true, field: 'hiddenfield'},
        {name: 'qtpp_wsdl_url', label: 'wsdl地址', show: true, field: 'textfield', value: qtpp_url},
        {name: 'qtpp_si_code', label: 'SI标识', show: true, field: 'textfield'},
        {name: 'qtpp_service_code', label: '业务代码', show: true, field: 'textfield'},
        {name: 'qtpp_ec_code', label: '集团编码', show: true, field: 'textfield'},
        {name: 'qtpp_fun_code', label: '功能点', show: true, field: 'textfield', blank: true},
        {name: 'qtpp_ser_code', label: '服务代码', show: true, field: 'textfield', blank: true},
        {name: 'qtpp_src_id', label: '源号码', show: true, field: 'textfield', blank: true},
        {name: 'qtpp_status', label: '端口状态',  field: 'combo', choice: 'qtpp.stat', value: 'enabled'},
        {name: 'qtpp_status_display', label: '端口状态', show: true},
        {name: 'qtpp_dept_id', label: '归属部门', field: 'combo', store: 'X.store.DeptStore'},
        {name: 'qtpp_dept', label: '归属部门', show: true}]
});