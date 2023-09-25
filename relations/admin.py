from django.contrib import admin
from relations.models import Review, Relation


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ('user', 'item', 'rate', 'text', 'parent')
    list_display = ('user', 'item', 'rate')


@admin.register(Relation)
class RatingAdmin(admin.ModelAdmin):
    fields = ('user', 'item', 'rate', 'in_liked')

    def save_model(self, request, obj, form, change):
        new_obj, _ = Relation.objects.get_or_create(
            user=obj.user, item=obj.item)
        new_obj.rate = obj.rate
        new_obj.in_liked = obj.in_liked
        new_obj.save()
