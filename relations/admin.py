from django.contrib import admin
from relations.models import Relation


@admin.register(Relation)
class RatingAdmin(admin.ModelAdmin):
    fields = ('user', 'item', 'rate', 'in_liked', 'comment', 'parent')

    def save_model(self, request, obj, form, change):
        new_obj, _ = Relation.objects.get_or_create(
            user=obj.user, item=obj.item)
        new_obj = obj
        new_obj.save()
