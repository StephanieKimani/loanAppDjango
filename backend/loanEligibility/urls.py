from django.urls import path,include
from . import views 
#from rest_framework.routers import DefaultRouter

#router = DefaultRouter()
#router.register("LoanDetail",views.LoanDetailApi)
#router.register("NewUser",views.UserDetailApi)

urlpatterns = [
  #path('api/',include(router.urls)),
  path('apilist/', views.loanList, name='loanapilist'),
  path('apicreate/', views.loanCreate, name='loanapilist'),
  path('apidetail/<str:pk>/', views.loanDetail, name='loanapidetail'),
  path('apiupdatedefault/<str:pk>/<str:accountNo>', views.updateDefault, name='updateDefault'),
  path('apiupdatestatus/<str:pk>/<str:status>', views.updateStatus, name='updateStatus'),
  path('apiupdaterepayed/<str:pk>/', views.updateRepayed, name='updateRepayed'),
  path('apistatus/<str:accountNo>/', views.getStatus, name='getStatus'),
]
