from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name="home"),
  path('single-sentiment/', views.single, name="single"),
  path('multiple-sentiment/', views.multi, name="multiple"),
]