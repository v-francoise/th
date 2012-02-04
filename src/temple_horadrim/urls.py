from dajaxice.core import dajaxice_autodiscover
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from temple_horadrim import settings

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

dajaxice_autodiscover()

urlpatterns = patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
    # Examples:
    # url(r'^$', 'temple_horadrim.views.home', name='home'),
    # url(r'^temple_horadrim/', include('temple_horadrim.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
                        { 'document_root': settings.MEDIA_ROOT }),
                       
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    # Uncomment the next line to enable the admin:
#    (r'^grappelli/', include('grappelli.urls')),
    (r'^ckeditor/', include('ckeditor.urls')),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/temple_horadrim/images/favicon.ico'}),
    url(r'^', include(admin.site.urls)),
)
