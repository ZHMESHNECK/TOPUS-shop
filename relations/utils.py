from django.contrib import messages
from relations.models import Relation
from relations.forms import AnswerForm, RelationForm
from products.utils import set_rating
import traceback


def accept_post(self, request, pk):
    fill_the_form = True   # чи потрібно автоматично заповняти форму

    # користувач підтвердив змінення відгугку
    if request.data.get('confirm', None):
        fill_the_form = False
        if pre_save(self, request, pk):
            messages.info(request, 'Успіх')
        else:
            messages.info(
                request, 'При створенні відгуку трапилася помилка :(')

    # staff дає відповідь на відгук
    elif request.data.get('parent', None):
        fill_the_form = False
        if pre_save(self, request, pk, answer=True):
            messages.info(request, 'Успіх')
        else:
            messages.info(
                request, 'При створенні відгуку трапилася помилка :(')

    # користувач выдаляє свій відгук
    elif request.data.get('delete_relation', None):
        fill_the_form = False
        if relation_delete(self, request, pk):
            messages.info(request, 'Успіх')
        else:
            messages.info(
                request, 'При видаленні відгуку трапилася помилка :(')
    else:
        form = RelationForm(request.data)
        relation = Relation.objects.filter(
            user_id=self.request.user.id, item_id=pk, parent__isnull=True)
        if form.is_valid():
            if len(relation) == 0:
                fill_the_form = False
                pre_save(self, request, pk)
                messages.info(request, 'Успіх')
            else:
                messages.info(
                    request, 'У вас вже є відгук на цей товар, якщо ви створите новий відгук - старий видалиться', extra_tags='1')
        else:
            messages.info(
                request, 'Вам потрібно обрати рейтинг для цього товару', extra_tags='2')
    if fill_the_form:
        parametrs = {
            "rate": form.cleaned_data.get('rate', None),
            "comment": form.cleaned_data['comment'],
            "form": form,
            "accept": True
        }
    else:
        parametrs = {
            "accept": True
        }
    return request, parametrs


def pre_save(self, request, pk, answer=False) -> bool:
    if answer:
        form = AnswerForm(request.data)
        if form.is_valid():
            form = form.save(commit=False)
            form.item_id = pk
            form.user_id = self.request.user.id
            form.parent_id = int(request.data.get('parent'))
            form.comment = request.data.get('comment')
            form.save()
            return True
        return False
    try:
        form = RelationForm(request.data)
        if form.is_valid():
            obj, _ = Relation.objects.get_or_create(
                user=request.user, item_id=pk, parent__isnull=True)
            obj.rate = request.data.get('rate')
            obj.comment = request.data.get('comment')
            obj.save()
            return True
        return False
    except:
        return False


def relation_delete(self, request, pk):
    try:
        relation = Relation.objects.get(
            user_id=request.user.id, item_id=pk, pk=int(request.data.get('delete_relation')))
        relation.delete()
        set_rating(relation.item)
        return True
    except:
        print(traceback.format_exc())
        return False
