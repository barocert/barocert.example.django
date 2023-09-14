# -*- coding: utf-8 -*-
try: 
    from django.conf.urls import url
except:
    from django.urls import re_path as url

from . import views

urlpatterns = [

    url(r'^RequestIdentity$', views.requestIdentityHandler, name='RequestIdentity'),
    url(r'^GetIdentityStatus$', views.getIdentityStatusHandler, name='GetIdentityStatus'),
    url(r'^VerifyIdentity$', views.verifyIdentityHandler, name='VerifyIdentity'),

    url(r'^RequestSign$', views.requestSignHandler, name='RequestSign'),
    url(r'^GetSignStatus$', views.getSignStatusHandler, name='GetSignStatus'),
    url(r'^VerifySign$', views.verifySignHandler, name='VerifySign'),

    url(r'^RequestMultiSign$', views.requestMultiSignHandler, name='RequestMultiSign'),
    url(r'^GetMultiSignStatus$', views.getMultiSignStateHandler, name='GetMultiSignStatus'),
    url(r'^VerifyMultiSign$', views.verifyMultiSignHandler, name='VerifyMultiSign'),

    url(r'^RequestCMS$', views.requestCMSHandler, name='RequestCMS'),
    url(r'^GetCMSStatus$', views.getCMSStatusHandler, name='GetCMSStatus'),
    url(r'^VerifyCMS$', views.verifyCMSHandler, name='VerifyCMS'),

    url(r'^VerifyLogin$', views.verifyLoginHandler, name='VerifyLogin'),

]
