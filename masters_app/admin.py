from django.contrib import admin
from .models import Master, Category, Work


# Register your models here.
class MasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'slug', 'category', 'about', 'photo', 'website', 'tg_id')
    list_display_links = ('id', 'firstname', 'lastname')
    search_fields = ('id', 'firstname', 'lastname')
    list_filer = ('category',)
    prepopulated_fields = {'slug': ('firstname', 'lastname')}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo', 'create_time', 'update_time')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filer = ('master',)


admin.site.register(Master, MasterAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Work, WorkAdmin)
