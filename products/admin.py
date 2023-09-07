from django.utils.safestring import mark_safe
from django.contrib import admin
from products.models import *
from products.utils import serial_code_randomizer


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
    list_display = ('title', 'category', 'main_image', 'is_published')
    list_filter = ('category', 'brand', 'price')
    list_editable = ('is_published',)
    search_fields = ('title', 'season', 'size')
    fields = ('title', 'description', 'price', 'category', 'brand',
              'main_image', 'is_published', 'size', 'season', 'department', 's_code', 'date_created')
    readonly_fields = ('s_code', 'date_created')
    inlines = [GalleryClInline]

    def get_html_photo(self, object):
        if object.main_image:
            return mark_safe(f'<img src="{object.main_image.url}" width=50>')

    get_html_photo.short_description = 'Зображення'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.s_code = serial_code_randomizer(obj.category)
        obj.save()


@admin.register(Gaming)
class GamingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'main_image', 'is_published')
    list_filter = ('category', 'brand', 'price')
    list_editable = ('is_published',)
    search_fields = ('title', 'brand', 'model')
    fields = ('title', 'description', 'price', 'category', 'brand',
              'main_image', 'is_published', 'material', 'model', 'color', 's_code')
    readonly_fields = ('s_code', 'date_created')
    inlines = [GalleryGaInline]

    def get_html_photo(self, object):
        if object.main_image:
            return mark_safe(f'<img src="./{object.main_image.url}" width=50>')

    get_html_photo.short_description = 'Изображение'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.s_code = serial_code_randomizer(obj.category)
        obj.save()


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'main_image', 'is_published')
    list_filter = ('category', 'brand', 'price')
    list_editable = ('is_published',)
    search_fields = ('title', 'room_type')
    fields = ('title', 'description', 'price', 'category', 'brand',
              'main_image', 'is_published', 'material', 'color', 'room_type', 'weight', 'dimensions', 's_code')
    readonly_fields = ('s_code', 'date_created')
    inlines = [GalleryHmInline]

    def get_html_photo(self, object):
        if object.main_image:
            return mark_safe(f'<img src="{object.main_image.url}" width=50>')

    get_html_photo.short_description = 'Изображение'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.s_code = serial_code_randomizer(obj.category)
        obj.save()


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass