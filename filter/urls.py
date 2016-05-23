from django.conf.urls import patterns, url
from X.tools.model import common_save, common_delete, common_list

urlpatterns = patterns(
    'filter.views',

    url(r'^cmpp2-list/$', common_list, {'model_type': 'filter.models.Cmpp2Cfg',
                                        'query_field': ['sock_source_ip', 'cmpp_sp_id', 'cmpp_src_id',
                                                        'cmpp_dept__name']}),
    url(r'^cmpp2-insert/$', common_save, {'model_type': 'filter.models.Cmpp2Cfg'}),
    url(r'^cmpp2-update/$', common_save, {'model_type': 'filter.models.Cmpp2Cfg'}),
    url(r'^cmpp2-delete/$', common_delete, {'model_type': 'filter.models.Cmpp2Cfg'}),

    url(r'^whitelist-list/$', common_list, {'model_type': 'filter.models.WhiteList',
                                            'query_field': ['src_id', 'name']}),
    url(r'^whitelist-insert/$', common_save, {'model_type': 'filter.models.WhiteList'}),
    url(r'^whitelist-update/$', common_save, {'model_type': 'filter.models.WhiteList'}),
    url(r'^whitelist-delete/$', common_delete, {'model_type': 'filter.models.WhiteList'}),

    url(r'^filter-list/(?P<stat>.+)/$', 'filter_list', {'query_field': ['name', 'text', 'note']}),
    url(r'^filter-insert/$', common_save, {'model_type': 'filter.models.Filter'}),
    url(r'^filter-update/$', common_save, {'model_type': 'filter.models.Filter'}),
    url(r'^filter-delete/$', common_delete, {'model_type': 'filter.models.Filter'}),
    url(r'^filter-audit/$', common_save, {'model_type': 'filter.models.Filter'}),
)
