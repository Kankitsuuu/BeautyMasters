from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, ListView

from .filters import MastersFilter
from .utils import DataMixin
from .forms import *

# Create your views here.


class HomeView(LoginRequiredMixin, DataMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

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
            'slug': form.cleaned_data['username']
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
        context.update(self.get_user_context())
        return context


class ChangePage(LoginRequiredMixin, DataMixin, View):
    login_url = '/login/'
    redirect_field_name = 'home'
    template_name = 'masters_app/change_page.html'

    def dispatch(self, request,  *args, **kwargs):
        page = get_object_or_404(Page, slug=kwargs['page_slug'])
        if request.method == 'POST':
            form = ChangePageForm(request.POST)
            if form.is_valid():
                try:
                    page.firstname = form.cleaned_data['firstname']
                    page.lastname = form.cleaned_data['lastname']
                    page.slug = form.cleaned_data['slug']
                    page.about = form.cleaned_data['about']
                    page.category = form.cleaned_data['category']
                    page.city = form.cleaned_data['city']
                    page.save()
                    return redirect('home')
                except Exception as e:
                    print(e)
                    form.add_error(None, 'Record change error')
        else:
            initial = {
                'firstname': page.firstname,
                'lastname': page.lastname,
                'slug': page.slug,
                'about': page.about,
                'category': page.category,
                'city': page.city
            }
            form = ChangePageForm(initial=initial)
            context = self.get_user_context(form=form, title='Змінити сторінку')
            return render(request, self.template_name, context)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context(title="Налаштування сторінки"))
        return context


class SearchView(DataMixin, View):

    def get(self, request, *args, **kwargs):
        page_list = Page.objects.all()
        page_filter = MastersFilter(request.GET, queryset=page_list)
        context = self.get_user_context(title='Beauty Masters')
        context.update({'filter': page_filter})
        return render(request, 'masters_app/search.html', context)

