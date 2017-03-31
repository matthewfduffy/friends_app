from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^main$', views.main, name='main'),
    url(r'^user/(?P<user_id>[^/]+)(?:/)*$', views.user, name="user"),
    url(r'^addfriend/(?P<user_id>[^/]+)(?:/)*$', views.newfriend, name="addfriend"),
	url(r'^deletefriend/(?P<user_id>[^/]+)(?:/)*$', views.byefriend, name="deletefriend"),
    url(r'^logout$', views.logout, name='logout'),
]
