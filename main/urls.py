from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
  path('', views.main, name='main'),
  path('api/provide_nearest_location/', views.provide_nearest_location, name='provide_nearest_location'),
]