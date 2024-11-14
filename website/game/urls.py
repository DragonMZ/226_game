from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('pick/<str:name>/<str:row>/<str:col>/', views.pick, name='pick'),
]