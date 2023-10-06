from django import forms
from relations.models import Relation


class RelationForm(forms.ModelForm):

    rate = forms.IntegerField(label='Оцінка')
    comment = forms.CharField(
        label='Текст', required=False)

    class Meta:
        model = Relation
        fields = ('rate', 'comment')

class AnswerForm(forms.ModelForm):

    comment = forms.CharField(
        label='Текст',required=True)

    class Meta:
        model = Relation
        fields = ('comment',)
