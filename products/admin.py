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
    list_display = ('id', 'cat_name', 'slug')
    list_display_links = ('cat_name',)


@admin.register(Clothes)
class ClothAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_html_photo',
                    's_code', 'is_published')
    list_filter = ('brand',)
    list_editable = ('is_published',)
    search_fields = ('title', 'season', 'size', 's_code')
    fields = ('title', 'description', 'price', 'discount', 'brand',
              'main_image', 'get_html_photo', 'is_published', 'size', 'season', 'department', 'rating', 's_code', 'date_created', 'owner')
    readonly_fields = ('s_code', 'date_created', 'owner',
                       'get_html_photo', 'rating')
    inlines = [GalleryClInline]

    def get_html_photo(self, object):
        if object.main_image:
            return mark_safe(f'<img src="{object.main_image.url}" width=50>')

    get_html_photo.short_description = 'Попередній перегляд'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        if not obj.category:
            obj.category = Category.objects.get(pk=1)
        if not obj.s_code or len(obj.s_code) < 10:
            obj.s_code = serial_code_randomizer(obj.category)
        obj.save()


@admin.register(Gaming)
class GamingAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_html_photo',
                    's_code', 'is_published')
    list_filter = ('brand',)
    list_editable = ('is_published',)
    search_fields = ('title', 'brand', 'model', 's_code')
    fields = ('title', 'description', 'price', 'discount', 'brand',
              'main_image', 'get_html_photo', 'is_published', 'material', 'model', 'color', 'rating', 's_code', 'date_created', 'owner')
    readonly_fields = ('s_code', 'date_created', 'owner',
                       'get_html_photo', 'rating', 'category')
    inlines = [GalleryGaInline]

    def get_html_photo(self, object):
        if object.main_image:
            return mark_safe(f'<img src="{object.main_image.url}" width=50>')

    get_html_photo.short_description = 'Попередній перегляд'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        if not obj.category:
            obj.category = Category.objects.get(pk=2)
        if not obj.s_code or len(obj.s_code) < 10:
            obj.s_code = serial_code_randomizer(obj.category)
        obj.save()


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_html_photo',
                    's_code', 'is_published')
    list_filter = ('brand',)
    list_editable = ('is_published',)
    search_fields = ('title', 'room_type', 's_code')
    fields = ('title', 'description', 'price', 'discount', 'brand',
              'main_image', 'get_html_photo', 'is_published', 'material', 'color', 'room_type', 'weight', 'dimensions', 'rating', 's_code', 'date_created', 'owner')
    readonly_fields = ('s_code', 'date_created', 'owner',
                       'get_html_photo', 'rating')
    inlines = [GalleryHmInline]

    def get_html_photo(self, object):
        if object.main_image:
            return mark_safe(f'<img src="{object.main_image.url}" width=50>')

    get_html_photo.short_description = 'Попередній перегляд'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        if not obj.category:
            obj.category = Category.objects.get(pk=3)
        if not obj.s_code or len(obj.s_code) < 10:
            obj.s_code = serial_code_randomizer(obj.category)
        obj.save()
