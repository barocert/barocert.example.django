"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
try: 
    from django.conf.urls import url
except:
    from django.urls import re_path as url
from django.conf.urls import include

from config.views import Index

urlpatterns = [
    url(r'^$', Index.as_view(), name='Index'),
    url(r'^KakaocertService/', include('KakaocertExample.urls'), name='KakaocertExample'),
    url(r'^NavercertService/', include('NavercertExample.urls'), name='NavercertExample'),
    url(r'^PasscertService/', include('PasscertExample.urls'), name='PasscertExample'),
]
