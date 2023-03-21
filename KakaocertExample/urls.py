# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^RequestESign$', views.requestESignHandler, name='RequestESign'),

    url(r'^BulkReqeustESign$', views.bulkReqeustESignHandler, name='BulkReqeustESign'),

    url(r'^GetESignState$', views.getESignStateHandler, name='GetESignState'),

    url(r'^GetBulkESignState$', views.getBulkESignStateHandler, name='GetBulkESignState'),

    url(r'^VerifyESign$', views.verifyESignHandler, name='VerifyESign'),

    url(r'^BulkVerifyESign$', views.bulkVerifyESignHandler, name='BulkVerifyESign'),

    url(r'^RequestVerifyAuth$', views.requestVerifyAuthHandler, name='RequestVerifyAuth'),

    url(r'^GetVerifyAuthState$', views.getVerifyAuthStateHandler, name='GetVerifyAuthState'),

    url(r'^VerifyAuth$', views.verifyAuthHandler, name='VerifyAuth'),

    url(r'^RequestCMS$', views.requestCMSHandler, name='RequestCMS'),

    url(r'^GetCMSState$', views.getCMSStateHandler, name='GetCMSState'),

    url(r'^VerifyCMS$', views.verifyCMSHandler, name='VerifyCMS'),

]
