from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from testserver import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'input/?$', views.input_values)
)
