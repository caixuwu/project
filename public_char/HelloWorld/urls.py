"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
# from django.conf.urls import url,include
# admin.autodiscover()
from django.views.static import serve
import os
#from HelloWorld import settings
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings

# from . import view
from books import views
 

#patterns('',
urlpatterns = [
    #(r'^search-from/$',views.search_from),
    #(r'^search/$',views.search),
    url(r'^admin/', admin.site.urls),
    url(r"^dmy.html/$",views.dmy,name='dmy.html'),
    url(r"^register.html/$",views.register,name='register'),
    #(r"^login/$",views.login),
    url(r'^index.html/$',views.index ,name='index.html'),
    url(r'^send_msg/$',views.send_msg),
    url(r'^get_msg/$',views.get_msg),
    url(r'^file_upload/$',views.file_upload,name='file_upload'),
    url(r'^forget/$', views.ForgetPassword, name='forget'),
    url(r'^reset_pwd/(?P<reset_code>\w+)/$', views.Reset_pwd.as_view(), name='Reset_pwd'),
    url(r'^modify_pwd/$', views.Modify_pwd.as_view(), name='Modify_pwd'),

                  # url(r'^uploads/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_URL }),
    # url(r'^images/(?P<path>.*)$' , 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS}),
    #(r'^js/(?P.*)$' , 'django.views.static.serve', {'document_root':  settings.STATICFILES_DIRS }),
    # (r'^Cbv/$',views.Cbv.as_view()),
    ]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


























# import settings
# urlpatterns = patterns('',
#     url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_URL }), 
# )
# urlpatterns += staticfiles_urlpatterns()