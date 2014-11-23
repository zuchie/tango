from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
#	url(r'^modify_definition/$', views.modify_definition, name='modify_definition'), 
)
