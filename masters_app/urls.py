from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<slug:page_slug>', views.PageView.as_view(), name='show_page'),
    path('page/settings/', views.ChangePage.as_view(), name='settings'),
    path('account/settings/', views.EditAccount.as_view(), name='account'),
    path('account/password-change/', views.PasswordChangeView.as_view(), name='password-change'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('album/<int:album_id>', views.AlbumContentView.as_view(), name='album'),
    path('work/<int:work_id>', views.WorkView.as_view(), name='work'),
    path('links/', views.LinksView.as_view(), name='links'),
    path('<slug:page_slug>/albums/', views.AlbumsView.as_view(), name='albums'),
    path('album/<int:album_id>/edit/', views.AlbumEditView.as_view(), name='album-edit'),
    path('album/add/', views.AlbumAddView.as_view(), name='album-add'),
    path('work/<int:work_id>/edit/', views.WorkEditView.as_view(), name='work-edit'),
    path('album/<int:album_id>/work/add', views.WorkAddView.as_view(), name='work-add'),
]
