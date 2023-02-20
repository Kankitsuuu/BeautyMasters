from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<slug:page_slug>', views.PageView.as_view(), name='show_page'),
    path('<slug:page_slug>/settings/', views.ChangePage.as_view(), name='settings'),
    path('<slug:page_slug>/settings/account/', views.EditAccount.as_view(), name='account'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<slug:page_slug>/albums/<int:album_id>', views.AlbumView.as_view(), name='album'),
    path('<slug:page_slug>/work/<int:work_id>', views.work_view, name='work')
]
