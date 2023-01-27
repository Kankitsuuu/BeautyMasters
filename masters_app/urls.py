from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<slug:master_slug>', views.master_page, name='show_master'),
    path('register/', views.register, name='register'),
    path('<slug:master_slug>/settings/', views.edit_master_page, name='settings'),
    path('search/', views.search_master, name='search'),
]