from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name="home"),
  path('single/with-emoji-and-emoticon', views.view_single_with, name="single_with"),
  path('single/without-emoji-and-emoticon', views.view_single_without, name="single_without"),
  path('multiple/', views.multi, name="multiple"),
]