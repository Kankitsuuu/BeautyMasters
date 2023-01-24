from django.db import models
from django.urls import reverse


# Create your models here.
class Master(models.Model):
    firstname = models.CharField(max_length=255, verbose_name='Name')
    lastname = models.CharField(max_length=255, verbose_name='Surname')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Category')
    about = models.TextField(verbose_name='About')
    photo = models.ImageField(upload_to="photos/masters/%Y/", verbose_name='Photo')
    website = models.URLField(blank=True, verbose_name='Website')
    tg_id = models.IntegerField(unique=True, blank=True, verbose_name='Telegram ID')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Last update')

    class Meta:
        verbose_name = 'Master'
        verbose_name_plural = 'Masters'

    def __str__(self):
        return self.firstname + ' ' + self.lastname

    def get_absolute_url(self):
        return reverse('show_master', kwargs={'master_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category Name')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories', kwargs={'category_slug': self.slug})


class Work(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    master = models.ForeignKey('Master', on_delete=models.CASCADE, verbose_name='Master')
    photo = models.ImageField(upload_to="photos/works/%Y/%m/%d/", verbose_name='Photo')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Last update')

    class Meta:
        verbose_name = 'Work'
        verbose_name_plural = 'Works'

    def __str__(self):
        return self.name

