from django.urls import path
from . import views
from .views import set_model_type

urlpatterns = [
  path('', views.home, name="home"),
  path('single/with-emoji-and-emoticon', views.view_single_with, name="single_with"),
  path('single/without-emoji-and-emoticon', views.view_single_without, name="single_without"),
  path('multiple', views.view_multi, name="multiple"),
  path('multiple/results', views.view_multi_result, name="multiple_result"),
  path('multiple/results_download', views.view_multi_result2, name="multiple_result2"),
  path('set_model_type/', set_model_type, name='set_model_type'),
]