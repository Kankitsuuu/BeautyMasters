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
    path('<slug:page_slug>/albums/<int:album_id>', views.AlbumContentView.as_view(), name='album'),
    path('work/<int:work_id>', views.WorkView.as_view(), name='work'),
    path('<slug:page_slug>/links/', views.LinksView.as_view(), name='links'),
    path('<slug:page_slug>/albums/', views.AlbumsView.as_view(), name='albums'),
    path('<slug:page_slug>/albums/<int:album_id>/edit/', views.AlbumEditView.as_view(), name='album-edit'),
    path('<slug:page_slug>/albums/add/', views.AlbumAddView.as_view(), name='album-add'),
]
