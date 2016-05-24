from django.conf.urls import patterns, url
# from spyne.server.django import DjangoView
# from api.wxlt_service import application
from api.wxlt_service import service as wxlt_service
from api.http_service import send_sms

urlpatterns = patterns(
    'api.views',
    # Examples:
    # url(r'^$', 'X.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^get-token/(.+)/$', 'get_token'),
    url(r'^send-sms/$', 'send_sms'),
    url(r'^recv-sms/$', 'recv_sms'),
    url(r'^status-report/$', 'status_report'),
    url(r'^test/(.+)/$', 'test'),
    # url(r'^wxlt_service/', DjangoView.as_view(application=application)),
    url(r'^wxlt_service/', wxlt_service),
    url(r'^http_service/', send_sms),
)
