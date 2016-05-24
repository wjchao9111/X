from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^base/', include('base.urls')),
    url(r'^addr/', include('addr.urls')),
    url(r'^sms/', include('sms.urls')),
    url(r'^filter/', include('filter.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^$', 'X.views.static', {'template': 'index.html'}),
    url(r'^su/$', 'X.views.su'),
)

urlpatterns += staticfiles_urlpatterns()
