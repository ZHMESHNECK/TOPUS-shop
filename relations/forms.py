from django import forms
from relations.models import Relation


class RelationForm(forms.ModelForm):

    rate = forms.IntegerField(label='Пароль')
    comment = forms.CharField(
        label='Текст', required=False)

    class Meta:
        model = Relation
        fields = ('rate', 'comment')
