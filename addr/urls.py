from django.conf.urls import patterns, url
from X.tools.model import common_list, common_save, common_delete

urlpatterns = patterns(
    'addr.views',
    url(r'^grp-tree/$', 'grp_tree'),
    url(r'^addr-file/$', 'addr_file'),
    url(r'^grp-list/$', common_list, {'model_type': 'addr.models.AddressGroup', 'query_field': ['name']}),
    url(r'^grp-insert/$', common_save, {'model_type': 'addr.models.AddressGroup'}),
    url(r'^grp-update/$', common_save, {'model_type': 'addr.models.AddressGroup'}),
    url(r'^grp-delete/$', common_delete, {'model_type': 'addr.models.AddressGroup'}),
    url(r'^addr-list/$', 'addr_list', {'grp_id': 0, 'query_field': ['phone', 'name']}),
    url(r'^addr-list/(?P<export>export)/$', 'addr_export', {'grp_id': 0}),
    url(r'^addr-list/(?P<grp_id>\d+)/$', 'addr_list', {'query_field': ['phone', 'name']}),
    url(r'^addr-list/(?P<grp_id>\d+)/(?P<export>export)/$', 'addr_export', {}),
    url(r'^addr-insert/$', common_save, {'model_type': 'addr.models.Address'}),
    url(r'^addr-update/$', common_save, {'model_type': 'addr.models.Address'}),
    url(r'^addr-delete/$', common_delete, {'model_type': 'addr.models.Address'}),
)
