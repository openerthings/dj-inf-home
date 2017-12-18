from django.conf.urls import url
from . import views

app_name = 'item'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rfid/$', views.listRFId, name='list_rfid'),
    url(r'^register/$', views.register, name='register'),
    url(r'^item_in/$', views.item_in, name='item_in'),
    url(r'^item_out/$', views.item_out, name='item_out'),
    url(r'^create_rfid/$', views.create_rfid, name='create_rfid'),
    url(r'^rfids_add/$', views.rfids_add, name='rfids_add'),
    url(r'^rfids_out/$', views.rfids_out, name='rfids_out'),
    url(r'^rfids_in/$', views.rfids_in, name='rfids_in'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<rfid_rf_id>[A-Z0-9]+)/$', views.detail, name='detail'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.rfiddets, name='rfiddets'),
    url(r'^(?P<rfid_rf_id>[A-Z0-9]+)/create_rfiddet/$', views.create_rfiddet, name='create_rfiddet'),
    url(r'^(?P<rfid_rf_id>[A-Z0-9]+)/delete_rfiddet/(?P<rfiddet_id>[0-9]+)/$', views.delete_rfiddet, name='delete_rfiddet'),
    url(r'^(?P<rfid_rf_id>[A-Z0-9]+)/delete_rfid/$', views.delete_rfid, name='delete_rfid'),
]
