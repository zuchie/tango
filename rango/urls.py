from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^add_item/$', views.add_item, name='add_item'),
        url(r'^modify_item/$', views.modify_item, name='modify_item'),
)
