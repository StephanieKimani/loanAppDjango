from django.urls import path,include
from . import views 

# Urls return various views upon being added to user/ in the main url.py file 
urlpatterns = [
    path('apilist/', views.userList, name='clientapilist'),
    path('apidetail/<str:pk>/', views.userDetail, name='clientapidetail'),
    path('apicreate/', views.userCreate, name='clientapicreate'),
    path('apilogin/', views.TokenObtainView.as_view(), name='login'),
    path('apiupdate/<str:pk>/', views.userUpdate, name='clientapiupdate'),
    path('apidelete/<str:pk>/', views.userDelete, name='clientapidelete'),
    path('hello/', views.clientProcess, name='client'),
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.authtoken')),
]
