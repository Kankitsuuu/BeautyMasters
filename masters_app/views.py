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
        print(user)
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


class AlbumView(DataMixin, View):
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


def work_view(request, page_slug, work_id):
    return HttpResponse(f'Work place {page_slug}, {work_id}')


