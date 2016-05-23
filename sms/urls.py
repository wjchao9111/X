from django.conf.urls import patterns, url
from X.tools.model import common_list, common_save, common_delete

urlpatterns = patterns(
    'sms.views',

    url(r'^task-insert/$', 'task_insert'),

    url(r'^processor-list/$', 'processor_list', {'pid': None, 'query_field': ['name']}),
    url(r'^processor-list-(?P<pid>\d+)/$', 'processor_list', {'query_field': ['name']}),
    url(r'^processor-update/$', 'processor_update'),
    url(r'^processor-delete/$', 'processor_delete'),

    url(r'^cmpp2-list/$', common_list, {'model_type': 'sms.models.Cmpp2Cfg',
                                        'query_field': ['sock_source_ip', 'cmpp_sp_id', 'cmpp_src_id',
                                                        'cmpp_sign_zh']}),
    url(r'^cmpp2-insert/$', common_save, {'model_type': 'sms.models.Cmpp2Cfg'}),
    url(r'^cmpp2-update/$', common_save, {'model_type': 'sms.models.Cmpp2Cfg'}),
    url(r'^cmpp2-delete/$', common_delete, {'model_type': 'sms.models.Cmpp2Cfg'}),

    url(r'^qtpp-list/$', common_list, {'model_type': 'sms.models.QtppCfg', 'query_field': ['qtpp_si_code']}),
    url(r'^qtpp-insert/$', common_save, {'model_type': 'sms.models.QtppCfg'}),
    url(r'^qtpp-update/$', common_save, {'model_type': 'sms.models.QtppCfg'}),
    url(r'^qtpp-delete/$', common_delete, {'model_type': 'sms.models.QtppCfg'}),

    url(r'^section-list/$', common_list,
        {'model_type': 'sms.models.CarrierSection', 'query_field': ['section', 'carrier']}),
    url(r'^section-insert/$', common_save, {'model_type': 'sms.models.CarrierSection'}),
    url(r'^section-update/$', common_save, {'model_type': 'sms.models.CarrierSection'}),
    url(r'^section-delete/$', common_delete, {'model_type': 'sms.models.CarrierSection'}),

    url(r'^api-user-list/$', 'api_user_list', {'query_field': ['code', 'name']}),
    url(r'^wxlt-user-list/$', 'wxlt_user_list', {'query_field': ['code', 'name']}),
    url(r'^wxlt-list/$', common_list, {'model_type': 'api.models.WxltConfig', 'query_field': ['pinid']}),
    url(r'^wxlt-insert/$', common_save, {'model_type': 'api.models.WxltConfig'}),
    url(r'^wxlt-update/$', common_save, {'model_type': 'api.models.WxltConfig'}),
    url(r'^wxlt-delete/$', common_delete, {'model_type': 'api.models.WxltConfig'}),

    url(r'^task-list/$', 'task_list', {'month': 0, 'query_field': ['name']}),
    url(r'^task-list/(?P<export>export)/$', 'task_export', {'month': 0}),
    url(r'^task-list-(?P<month>\d+)/$', 'task_list', {'query_field': ['name']}),
    url(r'^task-list-(?P<month>\d+)/(?P<export>export)/$', 'task_export', {}),

    url(r'^msg-send-count/$', 'msg_send_count'),
    url(r'^msg-send-list/$', 'msg_send_list', {'month': 0, 'task_id': 0, 'query_field': ['dest_terminal_id']}),
    url(r'^msg-send-list/(?P<export>export)/$', 'msg_send_export', {'month': 0, 'task_id': 0}),
    url(r'^msg-send-list/(?P<report>report)/$', 'msg_send_report', {'month': 0, 'task_id': 0}),
    url(r'^msg-send-list-(?P<month>\d+)/$', 'msg_send_list', {'task_id': 0, 'query_field': ['dest_terminal_id']}),
    url(r'^msg-send-list-(?P<month>\d+)/(?P<export>export)/$', 'msg_send_export', {'task_id': 0}),
    url(r'^msg-send-list-(?P<month>\d+)/(?P<report>report)/$', 'msg_send_report', {'task_id': 0}),
    url(r'^msg-send-list-(?P<month>\d+)/(?P<task_id>\d+)/$', 'msg_send_list', {'query_field': ['dest_terminal_id']}),
    url(r'^msg-send-list-(?P<month>\d+)/(?P<task_id>\d+)/(?P<export>export)/$', 'msg_send_export', {}),
    url(r'^msg-send-list-(?P<month>\d+)/(?P<task_id>\d+)/(?P<report>report)/$', 'msg_send_report', {}),
    url(r'^msg-recv-list/$', common_list, {'model_type': 'sms.models.MsgRecv', 'query_field': ['src_terminal_id']}),
)
