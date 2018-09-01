from app01 import views
from django.conf.urls import url
from app01 import views

urlpatterns = [
    url(r'^register', views.register),
    url(r'^login', views.login),
    url(r'^charbox', views.charbox),
    url(r'^echo', views.echo),

]