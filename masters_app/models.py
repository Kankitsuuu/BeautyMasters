from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Page(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', unique=True)
    firstname = models.CharField(max_length=255, verbose_name='Name')
    lastname = models.CharField(max_length=255, verbose_name='Surname')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Category', null=True)
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='City', null=True)
    about = models.TextField(verbose_name='About', blank=True)
    user_photo = models.ImageField(upload_to="photos/users/%Y/", verbose_name='Photo',
                                   default='photos/default/user_photo.jpg')
    tg_id = models.IntegerField(unique=True, verbose_name='Telegram ID', null=True)
    background = models.ImageField(upload_to="wallpapers/users/%Y", verbose_name="Background",
                                   default='wallpapers/default/page_background.jpg')

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return self.firstname + ' ' + self.lastname

    def get_absolute_url(self):
        return reverse('show_page', kwargs={'page_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category name')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=255, verbose_name='Album name')
    description = models.TextField(verbose_name='Description', blank=True)
    main_picture = models.ImageField(upload_to="photos/albums/%Y/", verbose_name='Main picture',
                                     default='photos/default/album_main.jpg')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Update time')
    page = models.ForeignKey('Page', on_delete=models.CASCADE, verbose_name='Page')

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

    def __str__(self):
        return self.name


class Work(models.Model):
    album = models.ForeignKey('Album', on_delete=models.CASCADE, verbose_name='Album')
    photo = models.ImageField(upload_to="photos/works/%Y/%m/%d/", verbose_name='Photo')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Add time')

    class Meta:
        verbose_name = 'Work'
        verbose_name_plural = 'Works'


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name='City')

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Link(models.Model):
    url = models.URLField(verbose_name='URL')
    link_type = models.ForeignKey('LinkType', on_delete=models.CASCADE, verbose_name='link type')
    page = models.ForeignKey('Page', on_delete=models.CASCADE, verbose_name='Page')

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    def __str__(self):
        return self.link_type


class LinkType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Site name')
    css_class = models.CharField(max_length=255, verbose_name='Link Type')

    class Meta:
        verbose_name = 'Link type'
        verbose_name_plural = 'Link types'

    def __str__(self):
        return self.name