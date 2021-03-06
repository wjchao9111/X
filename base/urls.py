from django.conf.urls import patterns, url
from X.tools.model import common_list, common_save, common_delete

urlpatterns = patterns(
    'base.views',
    url(r'^user-verify-(.+)/$', 'user_verify'),
    url(r'^user-login/$', 'user_login'),
    url(r'^user-logout/$', 'user_logout'),
    url(r'^user-info/$', 'user_info'),
    url(r'^user-perm/$', 'user_perm'),
    url(r'^role-perm/$', 'role_perm'),
    url(r'^role-perm-update/$', 'role_perm_update'),
    url(r'^user-reset-pass/$', 'user_reset_pass'),
    url(r'^user-list/$', common_list,
        {'model_type': 'base.models.User', 'query_field': ['code', 'name'], 'hide_field': ['pwd']}),
    url(r'^user-insert/$', common_save, {'model_type': 'base.models.User', 'protected_field': ['pwd']}),
    url(r'^user-update/$', common_save, {'model_type': 'base.models.User', 'protected_field': ['pwd']}),
    url(r'^user-delete/$', common_delete, {'model_type': 'base.models.User'}),
    url(r'^role-list/$', common_list,
        {'model_type': 'base.models.Role', 'query_field': ['name']}),
    url(r'^role-insert/$', common_save, {'model_type': 'base.models.Role', 'protected_field': ['pwd']}),
    url(r'^role-update/$', common_save, {'model_type': 'base.models.Role', 'protected_field': ['pwd']}),
    url(r'^role-delete/$', common_delete, {'model_type': 'base.models.Role'}),
    url(r'^perm-list/$', common_list,
        {'model_type': 'base.models.Permission', 'query_field': ['code', 'name']}),
    url(r'^perm-insert/$', common_save, {'model_type': 'base.models.Permission', 'protected_field': ['pwd']}),
    url(r'^perm-update/$', common_save, {'model_type': 'base.models.Permission', 'protected_field': ['pwd']}),
    url(r'^perm-delete/$', common_delete, {'model_type': 'base.models.Permission'}),
    url(r'^dept-list/$', common_list,
        {'model_type': 'base.models.Dept', 'query_field': ['name']}),
    url(r'^dept-insert/$', common_save, {'model_type': 'base.models.Dept', 'protected_field': ['pwd']}),
    url(r'^dept-update/$', common_save, {'model_type': 'base.models.Dept', 'protected_field': ['pwd']}),
    url(r'^dept-delete/$', common_delete, {'model_type': 'base.models.Dept'}),
)
