from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^translate/$', views.translate_item, name='translate_item'),
        url(r'^add/(?P<input_text>.+)/$', views.add_item, name='add_item'),
        url(r'^modify/(?P<input_text>.+)/$', views.modify_item, name='modify_item'),
)
