from django.utils.safestring import mark_safe
from django.contrib import admin
from products.models import *


class GalleryClInline(admin.TabularInline):
    fk_name = 'clothes_id'
    model = Gallery_cloth


class GalleryGaInline(admin.TabularInline):
    fk_name = 'gaming_id'
    model = Gallery_gaming


class GalleryHmInline(admin.TabularInline):
    fk_name = 'home_id'
    model = Gallery_home


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat_name',)
    list_display_links = ('cat_name',)
    prepopulated_fields = {'slug': ('cat_name',)}


@admin.register(Clothes)
class ClothAdmin(admin.ModelAdmin):
    list_display = ('title', 'category','main_image', 'get_html_photo', 'is_published')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'season', 'size')
    inlines = [GalleryClInline]

    def get_html_photo(self, object):
        if object.main_image:
            return mark_safe(f'<img src="{object.main_image.url}" width=50>')

    get_html_photo.short_description = 'Зображення'


@admin.register(Gaming)
class GamingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'get_html_photo', 'is_published')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryGaInline]

    def get_html_photo(self, object):
        if object.main_image:
            return mark_safe(f'<img src="./{object.main_image.url}" width=50>')

    get_html_photo.short_description = 'Изображение'


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'get_html_photo', 'is_published')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryHmInline]
    def get_html_photo(self, object):
        if object.main_image:
            return mark_safe(f'<img src="{object.main_image.url}" width=50>')

    get_html_photo.short_description = 'Изображение'
