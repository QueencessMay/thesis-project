from django.urls import path
from . import views

urlpatterns = [
  path('', views.view_home, name="home"),
  path('with-emoji-and-emoticon/', views.view_single_with, name="single_with"),
  path('without-emoji-and-emoticon/', views.view_single_without, name="single_without"),
  path('<str:option>/multiple/', views.view_multi, name="multiple"),
  path('<str:option>/multiple/results/', views.view_multi_result, name="multiple_result"),
  path('<str:option>/multiple/results/download/', views.download_result, name="download"),
]