from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
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
        print(context)
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
        context['albums'] = Album.objects.filter(page=context['page'])
        context['links'] = Link.objects.filter(page=context['page'])
        context.update(self.get_user_context())
        return context


class ChangePage(LoginRequiredMixin, DataMixin, View):
    login_url = '/login/'
    redirect_field_name = 'home'
    template_name = 'masters_app/change_page.html'

    def dispatch(self, request,  *args, **kwargs):
        page = get_object_or_404(Page, slug=kwargs['page_slug'])
        if request.method == 'POST':
            form = ChangePageForm(instance=request.user.page, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')

        else:
            form = ChangePageForm(instance=request.user.page)
        context = self.get_user_context(form=form, title='Змінити сторінку', page=page)
        return render(request, self.template_name, context)


class SearchView(DataMixin, View):

    def get(self, request, *args, **kwargs):
        page_list = Page.objects.all()
        page_filter = MastersFilter(request.GET, queryset=page_list)
        context = self.get_user_context(title='Beauty Masters')
        context.update({'filter': page_filter})
        return render(request, 'masters_app/search.html', context)


class EditAccount(LoginRequiredMixin, DataMixin, View):
    login_url = '/login/'
    redirect_field_name = 'home'
    template_name = 'masters_app/edit_account.html'

    def dispatch(self, request, *args, **kwargs):
        page = get_object_or_404(Page, slug=kwargs['page_slug'])
        if request.method == 'POST':
            form = EditAccountForm(instance=request.user, data=request.POST)
            if form.is_valid():
                page.firstname = form.cleaned_data['first_name']
                page.lastname = form.cleaned_data['last_name']
                page.slug = form.cleaned_data['username'].lower()
                page.save()
                form.save()
                return redirect('home')
        else:
            form = EditAccountForm(instance=request.user)
        context = self.get_user_context(form=form, title='Налаштування аккаунта', page=page)
        return render(request, self.template_name, context)


class AlbumContentView(DataMixin, View):
    def get(self, request, *args, **kwargs):

        page = get_object_or_404(Page, slug=kwargs['page_slug'])
        album = get_object_or_404(Album, pk=kwargs['album_id'])
        # paginator
        page_obj = self.get_paginator(request, Work, 8, album=album)

        context = self.get_user_context(title=f'{album.name}',
                                        page=page,
                                        page_obj=page_obj
                                        )
        return render(request, 'masters_app/album.html', context)


class WorkView(DataMixin, DetailView):
    model = Work
    pk_url_kwarg = 'work_id'
    template_name = 'masters_app/work.html'
    context_object_name = 'work'

    def get_context_data(self, *, object_list=None, **kwargs):
        print(kwargs)
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
                                             queryset=queryset,
                                             page=page,
                                             prev_work=prev_work,
                                             next_work=next_work))

        return context


class LinksView(LoginRequiredMixin, DataMixin, ListView):
    def dispatch(self, request, *args, **kwargs):
        page = get_object_or_404(Page, slug=kwargs['page_slug'])
        links = Link.objects.filter(page=page)
        title = f'{page} links'
        context = self.get_user_context(page=page,
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
                return redirect('links', page_slug=page.slug)

            elif '_add_link' in request.POST:
                form = LinkForm(data=request.POST)
                if form.is_valid():
                    Link.objects.create(page=page,
                                        link_type=form.cleaned_data['link_type'],
                                        url=form.cleaned_data['url'])
                    return redirect('links', page_slug=page.slug)
                else:
                    print(form.data)
                    print(form.cleaned_data)
                    print('Error')

            elif '_add' in request.POST:
                form = LinkForm(initial={'page': page})
                context.update(form=form)

            elif '_delete' in request.POST:
                print(request.POST)
                link = Link.objects.get(pk=request.POST['_delete'])
                link.delete()
                return redirect('links', page_slug=page.slug)

        return render(request, 'masters_app/links.html', context)


class AlbumsView(DataMixin, View):
    def dispatch(self, request, *args, **kwargs):

        page = get_object_or_404(Page, slug=kwargs['page_slug'])
        albums = Album.objects.filter(page=page)
        links = Link.objects.filter(page=page)
        title = f'{page}: Альбоми'
        page_obj = self.get_paginator(request, Album, 3, page=page)
        context = self.get_user_context(title=title,
                                        page=page,
                                        albums=albums,
                                        links=links,
                                        page_obj=page_obj)
        return render(request, 'masters_app/user_albums.html', context)


class AlbumAddView(DataMixin, CreateView):
    form_class = AlbumForm
    template_name = 'masters_app/album_constructor.html'

    def dispatch(self, request, *args, **kwargs):
        self.page = Page.objects.get(slug=kwargs['page_slug'])
        return super(AlbumAddView, self).dispatch(request, args, kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title="Створення альбому", mark='add'))
        print(context)
        return context

    def form_valid(self, form):
        print('DATA', form.data)
        print('CLEANED DATA PIC', form.cleaned_data['main_picture'])
        album_data = {
            'name': form.cleaned_data['name'],
            'description': form.cleaned_data['description'],
            'main_picture': form.cleaned_data['main_picture'],
            'page': self.page
        }
        Album.objects.create(**album_data)
        return redirect('albums', self.page.slug)


class AlbumEditView(DataMixin, View):
    def dispatch(self, request, *args, **kwargs):

        page = get_object_or_404(Page, slug=kwargs['page_slug'])
        form = None
        album_id = kwargs['album_id']
        title = 'Налаштування альбома'

        context = self.get_user_context(form=form, page=page, title=title, mark='edit')

        # POST
        if request.method == 'POST':
            album = get_object_or_404(Album, pk=album_id)

            if '_delete' in request.POST:
                album.delete()
                return redirect('albums', page_slug=page.slug)

            form = AlbumForm(instance=album, data=request.POST, files=request.FILES)
            if form.is_valid():
                print('DATA:', form.data)
                print('CLEANED DATA:', form.cleaned_data)
                form.save()
                return redirect('albums', page_slug=page.slug)
            else:
                print('Error')

        # GET
        else:
            album = get_object_or_404(Album, pk=kwargs['album_id'])
            form = AlbumForm(instance=album)
            context = self.get_user_context(form=form,
                                            page=page,
                                            title=title,
                                            mark='edit',
                                            album_header=album.main_picture)

        return render(request, 'masters_app/album_constructor.html', context)






