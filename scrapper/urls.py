
from django.contrib import admin
from django.urls import path,include
from .facebook import create as fbcreate, facebook as facebook, sendmessage as fbsm
from .linkedin import create as lncreate, linkedin as linkedin, sendmessage as lnsm
from .views import * 
urlpatterns = [
    path('facebook/create', fbcreate,name="fbcreate"),
    path('facebook', facebook),    
    path('facebook/message', fbsm),

    path('linkedin/create', lncreate,name="lncreate"),
    path('linkedin/message/<int:pk>', lnsm),
    path('linkedin', linkedin),
    path('', dashboard),
]
