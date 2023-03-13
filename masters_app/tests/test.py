import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.test import RequestFactory, TestCase
from django.urls import reverse, reverse_lazy

from masters_app.forms import LinkForm, LoginUserForm, ChangePageForm
from masters_app.models import Page, Category, Album, Work, City, Link, LinkType
from masters_app.views import HomeView, LoginUser, PageView, RegisterUser, WorkView, WorkAddView, AlbumAddView


class MastersApplicationTest(TestCase):

    # CUSTOM HELP FUNCTIONS
    def setUp(self) -> None:
        self.user = User.objects.create(username='test_user', password='secretpassword90')
        self.category = self.create_category_object()
        self.city = self.create_city_object()
        self.page = self.create_page_object(self.user, self.category, self.city)
        self.album = self.create_album_object(self.page)
        self.work = self.create_work_object(self.album)
        self.link_type = self.create_link_type_object()
        self.link = self.create_link_object(self.link_type, self.page)

    def create_response(self, url, url_kwargs=None, method='GET', login=False, data=None):
        path = reverse(url, kwargs=url_kwargs)
        if login:
            self.client.force_login(self.user)

        if method == 'GET':
            response = self.client.get(path, data)
        else:
            response = self.client.post(path, data)

        return response

    def create_model(self, model, *args, **kwargs):
        return model.objects.create(**kwargs)

    def create_page_object(self, user, category, city, slug='test_slug'):
        photo = SimpleUploadedFile(name='test_image.jpg', content=b'some content',
                                            content_type='image/jpeg')
        kwargs = {
            'user': user,
            'firstname': 'test_name',
            'lastname': 'test_surname',
            'slug': slug,
            'category': category,
            'city': city,
            'about': 'test_about_text',
            'user_photo': photo,
            'background': photo,
        }
        page = self.create_model(Page, **kwargs)
        return page

    def create_category_object(self):
        return self.create_model(Category, name='test_category_object')

    def create_city_object(self):
        return self.create_model(City, name='test_city_name')

    def create_album_object(self, page):
        album = self.create_model(Album, name='test_album_name', description='test_description', page=page)
        album.main_picture.image = SimpleUploadedFile(name='test_image.jpg', content=b'some content',
                                            content_type='image/jpeg')
        return album

    # Possible problem with photo
    def create_work_object(self, album):
        work = self.create_model(Work, album=album, description='test_work_description', photo='img.jpg')
        work.photo.image = SimpleUploadedFile(name='test_image.jpg', content=b'some content',
                                            content_type='image/jpeg')
        return work

    def create_link_type_object(self):
        return self.create_model(LinkType, name='test_link_type', css_class='test_css_class')

    def create_link_object(self, link_type, page):
        return self.create_model(Link, url='https://www.youtube.com', link_type=link_type, page=page)

    # TESTS
    def test_model_creation(self):
        model = self.create_model(LinkType, name='test-link-type', css_class='test-css-class')
        self.assertIsInstance(model, LinkType)
        self.assertEqual('test-link-type', model.name)
        self.assertEqual('test-css-class', model.css_class)

    def test_page_model(self):
        expected = self.page.firstname + ' ' + self.page.lastname
        self.assertEqual(str(self.page), expected)
        # need to check absolute_url

    def test_category_model(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_city_model(self):
        self.assertEqual(str(self.city), self.city.name)

    def test_link_object(self):
        self.assertEqual(str(self.link), str(self.link.link_type))
        self.assertIsInstance(self.link.link_type, LinkType)

    def test_link_type_object(self):
        self.assertEqual(str(self.link_type), self.link_type.name)

    def test_album_object(self):
        self.assertEqual(str(self.album), self.album.name)

    # def test_work_object(self):
    #     work = self.create_work_object()
    #     # need to check absolute_url
    #     pass

    # TESTING FORMS
    def test_link_form(self):
        form = LinkForm()
        empty_label = form.fields['link_type'].empty_label
        self.assertEqual(empty_label, 'Тип посилання')

    # TESTING VIEWS
    # HomeView
    def test_home_view(self):
        url = reverse('home')
        resp = self.client.get(url)
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('title', resp.content.decode())

    def test_home_view_with_auth(self):
        self.client.force_login(self.user)
        url = reverse('home')
        resp = self.client.get(url)
        self.assertIsInstance(resp, HttpResponseRedirect)
        self.assertEqual(resp.status_code, 302)

    # LoginUser
    def test_login_user_view_GET(self):
        request = RequestFactory().get('/')
        view = LoginUser()
        view.setup(request)
        context = view.get_context_data()
        self.assertIn('title', context)
        self.assertIn('form', context)

    def test_login_user_view_POST(self):
        data = {'username': 'test-login-user', 'password':'testpass111'}
        User.objects.create(**data)
        url = reverse('login')
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

    # Logout
    def test_logout_user(self):
        self.client.force_login(user=self.user)
        url = reverse('logout')
        resp = self.client.get(url)
        self.assertIsInstance(resp, HttpResponseRedirect)
        self.assertEqual(resp.status_code, 302)

    # RegisterUser
    def test_register_user_view_GET(self):
        response = self.create_response(url='register')
        self.assertEqual(response.status_code, 200)
        self.assertIn('title', response.context)
        self.assertIn('form', response.context)

    def test_register_user_view_POST(self):
        data = {
            'username': 'test_register_user',
            'password1': 'test_reg_pass111',
            'password2': 'test_reg_pass111',
            'first_name': 'user_name',
            'last_name': 'user_lastname',
            'email': 'testuser111@gmail.com',
        }
        url = reverse('register')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    # PageView
    def test_page_view_GET(self):
        response = self.create_response(
            url='show_page',
            url_kwargs={'page_slug': self.page.slug}
        )
        self.assertIn('albums', response.context)
        self.assertIn('title', response.context)

    # ChangePage
    def test_change_page_view_GET(self):
        response = self.create_response(url='settings')
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_change_page_view_GET_with_auth(self):
        self.client.force_login(self.user)
        url = reverse('settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

    def test_change_page_view_POST(self):
        self.client.force_login(self.user)
        url = reverse('settings')
        category = self.create_category_object()
        city = self.create_city_object()
        category.name = 'test_change_category'
        category.save()
        city.name = 'test_change_city'
        city.save()
        data = {
            'firstname': 'test_change_name',
            'lastname': 'test_change_surname',
            'about': 'test_change_about_text',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        category.delete()
        city.delete()

    # SearchView
    def test_search_view(self):
        url = reverse('search')
        response = self.client.get(url, data={'_searched': 'True'})
        self.assertEqual(response.status_code, 200)

    # EditAccount
    def test_edit_account_GET(self):
        url = reverse('account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_edit_account_GET_with_auth(self):
        self.client.force_login(self.user)
        url = reverse('account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

    def test_edit_account_POST(self):
        self.client.force_login(self.user)
        url = reverse('account')
        data = {
            'username': 'account_change_username',
            'email': 'test_change_email@gmail.com',
            'first_name': 'test_change_name',
            'last_name': 'test_change_lastname'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)

    # AlbumContentView
    def test_album_content_view_GET(self):
        response = self.create_response(
            url='album',
            url_kwargs={'album_id': self.album.pk},
            login=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'masters_app/album.html')

    # WorkView
    def test_work_view_GET(self):
        for i in range(3):
            photo = SimpleUploadedFile(name=f'test_image{i}.jpg', content=b'some content',
                                            content_type='image/jpeg')
            initial = {
                'album': self.album,
                'photo': photo,
                'description': f'test_description_{i}',
            }
            Work.objects.create(**initial)
        response = self.create_response(
            url='work',
            url_kwargs={'work_id': self.work.pk},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('next_work', response.context)
        self.assertIn('page', response.context)

    # LinksView
    def test_links_view_GET(self):
        url = reverse('links')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_links_view_GET_with_auth(self):
        self.client.force_login(self.user)
        url = reverse('links')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        self.assertTemplateUsed(response, 'masters_app/links.html')

    def test_links_view_POST_edit(self):
        data = {'_edit': self.link.pk}
        response = self.create_response(url='links', method='POST', login=True, data=data)
        self.assertIsInstance(response, HttpResponse)
        self.assertTemplateUsed(response, 'masters_app/links.html')

    def test_links_view_POST_save(self):
        data = {
            '_save': self.link.pk,
        }
        response = self.create_response(url='links', method='POST', login=True, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_links_view_POST_add(self):
        data = {
            '_add': 'btn_add_new_link',
        }
        response = self.create_response(url='links', method='POST', login=True, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'masters_app/links.html')

    def test_links_view_POST_add_link(self):
        data = {
            '_add_link': 'btn_add_link',
            'link_type': self.link_type,
            'url': "https://www.instagram.com/kankitsuuu/"
        }
        response = self.create_response(url='links', method='POST', login=True, data=data)
        print(response.context)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)


    def test_links_view_POST_delete(self):
        data = {'_delete': self.link.pk}
        response = self.create_response(url='links', method='POST', login=True, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)

    # AlbumsView
    def test_albums_view_GET(self):
        response = self.create_response(
            url='albums',
            url_kwargs={'page_slug': self.page.slug},
            login=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('owner', response.context)
        self.assertIn('page_obj', response.context)

    # AlbumAddView
    def test_album_add_view_GET(self):
        response = self.create_response(url='album-add')
        self.assertEqual(response.status_code, 302)

    def test_album_add_view_GET_with_auth(self):
        response = self.create_response(
            url='album-add',
            login=True,
        )
        self.assertIn('mark', response.context)
        self.assertIn('page', response.context)

    def test_album_add_view_POST(self):
        data = {
            'name': 'album_add_name',
            'description': 'album_description',
        }
        response = self.create_response(
            url='album-add',
            method='POST',
            login=True,
            data=data
        )
        self.assertEqual(response.status_code, 302)

    # AlbumEditView
    def test_album_edit_view_GET(self):
        user = User.objects.create(username='test_u1', password='trewq12345')
        page = self.create_page_object(user, self.category, self.city, slug='second-slug')
        self.client.force_login(user)
        response = self.create_response(
            url='album-edit',
            url_kwargs={'album_id': self.album.pk},
        )
        self.assertEqual(response.status_code, 302)
        user.delete()
        page.delete()

    def test_album_edit_view_GET_with_auth(self):
        response = self.create_response(
            url='album-edit',
            url_kwargs={'album_id': self.album.pk},
            login=True
        )
        self.assertEqual(response.status_code, 200)

    def test_album_edit_view_POST(self):
        data = {
            'name': 'test_edit_album_name',
            'description': 'test_edit_album_description'
        }
        response = self.create_response(
            url='album-edit',
            url_kwargs={'album_id': self.album.pk},
            login=True,
            method='POST',
            data=data
        )
        self.assertEqual(response.status_code, 302)

    def test_album_edit_view_POST_delete(self):
        data = {
            '_delete': 'push_delete_button',
            'name': 'test_edit_album_name',
            'description': 'test_edit_album_description'
        }
        response = self.create_response(
            url='album-edit',
            url_kwargs={'album_id': self.album.pk},
            login=True,
            method='POST',
            data=data
        )
        self.assertEqual(response.status_code, 302)

    # WorkAddView
    def test_work_add_view_GET(self):
        user = User.objects.create(username='test_u1', password='trewq12345')
        page = self.create_page_object(user, self.category, self.city, slug='second-slug')
        self.client.force_login(user)
        response = self.create_response(
            url='work-add',
            url_kwargs={'album_id': self.album.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        user.delete()
        page.delete()

    def test_work_add_view_GET_with_auth(self):
        response = self.create_response(
            url='work-add',
            url_kwargs={'album_id': self.album.pk},
            login=True
        )
        self.assertIn('mark', response.context)
        self.assertIn('page', response.context)
        self.assertIn('album', response.context)

    def test_work_add_view_POST(self):
        image = tempfile.NamedTemporaryFile(suffix=".jpg")
        data = {
            'photo': image.name,
            'description': 'some-test-description',
        }
        response = self.create_response(
            url='work-add',
            url_kwargs={'album_id': self.album.pk},
            login=True,
            method='POST',
            data=data
        )
        # print(response.context)
        print(image.name)
        self.assertEqual(response.status_code, 302)

    # WorkEditView
    def test_work_edit_view_GET(self):
        user = User.objects.create(username='test_u1', password='trewq12345')
        page = self.create_page_object(user, self.category, self.city, slug='second-slug')
        self.client.force_login(user)
        response = self.create_response(
            url='work-edit',
            url_kwargs={'work_id': self.work.pk}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        user.delete()
        page.delete()

    def test_work_edit_view_GET_with_auth(self):
        response = self.create_response(
            url='work-edit',
            url_kwargs={'work_id': self.work.pk},
            login=True
        )
        self.assertEqual(response.status_code, 200)

    def test_work_edit_view_POST(self):
        photo = self.create_work_object(self.album)
        photo.image = SimpleUploadedFile(name='test_image.jpg',
                                       content=b'test_edit_image',
                                       content_type='image/jpeg')
        data = {
            'photo': photo,
            'description': 'test_work_description',
        }
        response = self.create_response(
            url='work-edit',
            url_kwargs={'work_id': self.work.pk},
            login=True,
            method='POST',
            data=data
        )
        self.assertEqual(response.status_code, 302)
        photo.delete()

    def test_work_edit_view_POST_delete(self):
        data = {
            '_delete': 'delete_work'
        }
        response = self.create_response(
            url='work-edit',
            url_kwargs={'work_id': self.work.pk},
            login=True,
            method='POST',
            data=data
        )
        self.assertEqual(response.status_code, 302)

    # PasswordChangeView
    def test_password_change_view_GET(self):
        response = self.create_response(url='password-change')
        self.assertEqual(response.status_code, 302)

    def test_password_change_view_GET_with_auth(self):
        response = self.create_response(url='password-change', login=True)
        self.assertEqual(response.status_code, 200)

    def test_password_change_view_POST(self):
        credentials = {'username': 'test_user', 'password': 'secretpassword90'}
        self.user.set_password(raw_password='secretpassword90')
        self.client.login(**credentials)
        url = 'password-change'
        data = {
            'old_password': 'secretpassword90',
            'new_password1': 'Bananabomb2208',
            'new_password2': 'Bananabomb2208',
        }
        response = self.create_response(url=url, method='POST', data=data)
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        self.user.delete()
        self.category.delete()
        self.city.delete()
        self.page.delete()
        self.album.delete()
        self.work.delete()
        self.link_type.delete()
        self.link.delete()






