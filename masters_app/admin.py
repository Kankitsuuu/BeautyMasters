from django.contrib import admin
from .models import Page, Category, Work, Album, City, Link, LinkType


# Register your models here.
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'slug', 'category', 'city', 'user_photo',  'tg_id')
    list_display_links = ('id',)
    search_fields = ('id', 'firstname', 'lastname')
    list_filter = ('category', 'city')
    prepopulated_fields = {'slug': ('firstname', 'lastname')}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_time')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'page', 'main_picture', 'create_time', 'update_time')
    list_display_links = ('id',  'page')
    list_filter = ('page',)


class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'album', 'photo', 'add_time')
    list_display_links = ('id', 'album')
    search_fields = ('album',)
    list_filter = ('album',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', )
    search_fields = ('name',)


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'page', 'link_type')
    list_display_links = ('id', 'page', 'link_type')
    list_filter = ('link_type',)


class LinkTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'css_class')
    list_display_links = ('id', 'name')


admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(LinkType, LinkTypeAdmin)
