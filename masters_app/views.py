from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, ListView

from .filters import MastersFilter
from .utils import DataMixin
from .forms import *


# Create your views here.
class HomeView(DataMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            page = Page.objects.get(user=request.user)
            slug = page.slug
            return redirect('show_page', slug)
        # else (user is not authenticated)
        context = self.get_user_context(title='Beauty Masters')
        return render(request, 'masters_app/home.html', context=context)


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'masters_app/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title="Авторизація"))
        return context


def logout_user(request):
    logout(request)
    return redirect('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'masters_app/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title="Реєстрація"))
        return context

    def form_valid(self, form):
        user = form.save()
        page_data = {
            'firstname': form.cleaned_data['first_name'],
            'lastname': form.cleaned_data['last_name'],
            'user': user,
            'slug': form.cleaned_data['username'].lower()
        }
        # save user data
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        # create page for user
        Page.objects.create(**page_data)
        login(self.request, user)
        return redirect('home')


class PageView(DataMixin, DetailView):
    model = Page
    template_name = 'masters_app/page.html'
    slug_url_kwarg = 'page_slug'
    context_object_name = 'page'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['page']
        context['albums'] = Album.objects.filter(page=context['page'])[:3]
        context.update(self.get_user_context())
        return context


class ChangePage( DataMixin, View):
    template_name = 'masters_app/change_page.html'

    def dispatch(self, request,  *args, **kwargs):
        user = request.user

        # checking authentication
        if not user.is_authenticated:
            return redirect('login')

        # POST
        if request.method == 'POST':
            form = ChangePageForm(instance=user.page, data=request.POST, files=request.FILES)
            print(request.FILES)
            if form.is_valid():
                user.first_name = form.cleaned_data['firstname']
                user.last_name = form.cleaned_data['lastname']
                user.save()
                form.save()
                return redirect('home')

        # GET
        else:
            form = ChangePageForm(instance=user.page)
        context = self.get_user_context(form=form, title='Змінити сторінку', page=user.page)
        return render(request, self.template_name, context)


class SearchView(DataMixin, View):

    def get(self, request, *args, **kwargs):
        page_list = Page.objects.all().select_related('category', 'city')
        page_filter = MastersFilter(request.GET, queryset=page_list)
        searched = False
        if '_search' in request.GET:
            searched = True
        context = self.get_user_context(title='Beauty Masters',
                                        filter=page_filter,
                                        searched=searched)
        return render(request, 'masters_app/search.html', context)


class EditAccount(DataMixin, View):
    template_name = 'masters_app/edit_account.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # checking authentication
        if not user.is_authenticated:
            return redirect('login')

        # POST
        if request.method == 'POST':
            form = EditAccountForm(instance=user, data=request.POST)
            if form.is_valid():
                user.page.firstname = form.cleaned_data['first_name']
                user.page.lastname = form.cleaned_data['last_name']
                user.page.slug = form.cleaned_data['username'].lower()
                user.page.save()
                form.save()
                return redirect('home')

        # GET
        else:
            form = EditAccountForm(instance=user)
        context = self.get_user_context(form=form, title='Налаштування аккаунта', page=user.page)
        return render(request, self.template_name, context)


class AlbumContentView(DataMixin, View):
    def get(self, request, *args, **kwargs):

        album = get_object_or_404(Album, pk=kwargs['album_id'])
        page = album.page
        owner = False
        if request.user.page == page:
            owner = True
        # paginator
        page_obj = self.get_paginator(request, Work, 8, album=album)

        context = self.get_user_context(title=f'{album.name}',
                                        page=page,
                                        page_obj=page_obj,
                                        album_id=album.pk,
                                        owner=owner
                                        )
        return render(request, 'masters_app/album.html', context)


class WorkView(DataMixin, DetailView):
    model = Work
    pk_url_kwarg = 'work_id'
    template_name = 'masters_app/work.html'
    context_object_name = 'work'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        album = context['work'].album
        page = album.page
        queryset = self.model.objects.filter(album=album)

        # finding prev and next work
        prev_work, next_work = None, None
        found = False
        for work in queryset:
            if found:
                next_work = work.pk
                break
            if work == context['work']:
                found = True
                continue
            prev_work = work.pk

        context.update(self.get_user_context(title=album,
                                             page=page,
                                             prev_work=prev_work,
                                             next_work=next_work))
        return context


class LinksView(DataMixin, ListView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # checking authentication
        if not user.is_authenticated:
            return redirect('login')

        links = Link.objects.filter(page=user.page).select_related('link_type')
        title = f'{user.page} links'
        context = self.get_user_context(page=user.page,
                                        links=links,
                                        title=title)
        if request.method == 'POST':

            if '_edit' in request.POST:
                link = Link.objects.get(pk=request.POST['_edit'])
                form = LinkForm(instance=link)
                context.update(form=form, mark=request.POST['_edit'])

            elif '_save' in request.POST:
                link = Link.objects.get(pk=request.POST['_save'])
                form = LinkForm(instance=link, data=request.POST)
                if form.is_valid():
                    form.save()
                else:
                    print('Error')
                return redirect('links')

            elif '_add_link' in request.POST:
                form = LinkForm(data=request.POST)
                if form.is_valid():
                    Link.objects.create(page=user.page,
                                        link_type=form.cleaned_data['link_type'],
                                        url=form.cleaned_data['url'])
                    return redirect('links')
                else:
                    form.add_error(None, 'Unknown Error')

            elif '_add' in request.POST:
                form = LinkForm(initial={'page': user.page})
                context.update(form=form)

            elif '_delete' in request.POST:
                link = Link.objects.get(pk=request.POST['_delete'])
                link.delete()
                return redirect('links')

        return render(request, 'masters_app/links.html', context)


class AlbumsView(DataMixin, View):
    def dispatch(self, request, *args, **kwargs):
        page = get_object_or_404(Page, slug=kwargs['page_slug'])
        owner = False
        if request.user.page == page:
            owner = True
        albums = Album.objects.filter(page=page)
        title = f'{page}: Альбоми'
        page_obj = self.get_paginator(request, Album, 3, page=page)
        context = self.get_user_context(title=title,
                                        page=page,
                                        albums=albums,
                                        page_obj=page_obj,
                                        owner=owner)
        return render(request, 'masters_app/user_albums.html', context)


class AlbumAddView(DataMixin, CreateView):
    form_class = AlbumForm
    template_name = 'masters_app/album_constructor.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        if not self.user.is_authenticated:
            return redirect('login')
        return super(AlbumAddView, self).dispatch(request, args, kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title="Створення альбому", mark='add', page=self.user.page))
        return context

    def form_valid(self, form):

        album_data = {
            'name': form.cleaned_data['name'],
            'description': form.cleaned_data['description'],
            'main_picture': form.cleaned_data['main_picture'],
            'page': self.user.page
        }
        Album.objects.create(**album_data)
        return redirect('albums', self.user.page.slug)


class AlbumEditView(DataMixin, View):
    def dispatch(self, request, *args, **kwargs):

        album = get_object_or_404(Album, pk=kwargs['album_id'])
        page = album.page

        # checking user
        if request.user.page != page:
            return redirect('home')

        title = 'Налаштування альбома'

        # POST
        if request.method == 'POST':
            if '_delete' in request.POST:
                album.delete()
                return redirect('albums', page_slug=page.slug)

            form = AlbumForm(instance=album, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect('albums', page_slug=page.slug)
            else:
                print('Error')

        # GET
        else:
            form = AlbumForm(instance=album)

        context = self.get_user_context(form=form,
                                        page=page,
                                        title=title,
                                        mark='edit',
                                        album_header=album.main_picture)
        return render(request, 'masters_app/album_constructor.html', context)


class WorkAddView(DataMixin, CreateView):
    form_class = WorkForm
    template_name = 'masters_app/work_constructor.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.album = None

    def dispatch(self, request, *args, **kwargs):
        self.album = get_object_or_404(Album, pk=kwargs['album_id'])

        # checking user
        if request.user.page != self.album.page:
            return redirect('home')

        return super(WorkAddView, self).dispatch(request, args, kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title="Додати роботу",
                                             page=self.album.page,
                                             album=self.album,
                                             mark='add'))
        return context

    def form_valid(self, form):
        work_data = {
            'photo': form.cleaned_data['photo'],
            'description': form.cleaned_data['description'],
            'album': self.album,
        }
        Work.objects.create(**work_data)

        return redirect('album', self.album.pk)


class WorkEditView(DataMixin, View):
    def dispatch(self, request, *args, **kwargs):

        work = get_object_or_404(Work, pk=kwargs['work_id'])
        album = work.album
        page = album.page

        # checking user
        if request.user.page != page:
            return redirect('home')

        title = 'Змінити роботу'

        # POST
        if request.method == 'POST':
            if '_delete' in request.POST:
                work.delete()
                return redirect('album', album_id=album.pk)
            form = WorkForm(instance=work, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect('work', work_id=work.pk)
            else:
                form.add_error(None, 'ERROR')

        # GET
        else:
            form = WorkForm(instance=work)

        context = self.get_user_context(form=form, page=page, album=album, title=title, mark='edit')
        return render(request, 'masters_app/work_constructor.html', context)


class PasswordChangeView(DataMixin, View):
    def dispatch(self, request, *args, **kwargs):
        # checking user
        if not request.user.is_authenticated:
            return redirect('login')

        if request.POST:
            form = PasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('account')
            else:
                form.add_error(None, 'ERROR')

        form = PasswordForm(user=request.user)
        title = 'Зміна пароля'
        context = self.get_user_context(form=form, page=request.user.page, title=title)
        return render(request, 'masters_app/password-change.html', context)
