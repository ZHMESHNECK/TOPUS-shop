from django.contrib import messages
from relations.models import Relation
from relations.forms import AnswerForm, RelationForm
from products.utils import set_rating


def accept_post(self, request, pk):
    """ Приймає post запит відгука та обробляє його 

    Args:
        request (_type_): запит
        pk (_type_): id товару

    Returns:
        request, parametrs: 
    """
    fill_the_form = True   # чи потрібно автоматично заповняти форму

    # користувач підтвердив змінення відгугку
    if request.data.get('confirm', None):
        fill_the_form = False
        if pre_save(self, request, pk):
            messages.success(request, 'Успіх, відгук змінено')
        else:
            messages.warning(
                request, 'При створенні відгуку трапилася помилка :(')

    # staff дає відповідь на відгук
    elif request.data.get('parent', None):
        fill_the_form = False
        if pre_save(self, request, pk, answer=True):
            messages.success(
                request, 'Успіх, відповідь додана')
        else:
            messages.warning(
                request, 'При створенні відгуку трапилася помилка :(')

    # користувач выдаляє свій відгук
    elif request.data.get('delete_relation', None):
        fill_the_form = False
        if relation_delete(self, request, pk):
            messages.success(request, 'Успіх, відгук видалено')
        else:
            messages.warning(
                request, 'При видаленні відгуку трапилася помилка :(')
    # додання відгуку
    else:
        form = RelationForm(request.data)
        relation = Relation.objects.filter(
            user_id=self.request.user.id, item_id=pk, parent__isnull=True)
        if form.is_valid():
            if len(relation) == 0:
                fill_the_form = False
                pre_save(self, request, pk)
                messages.success(
                    request, 'Успіх, відгук створено')
            else:
                messages.info(
                    request, 'У вас вже є відгук на цей товар, якщо ви створите новий відгук - старий видалиться', extra_tags='middle')
        else:
            fill_the_form = True
            messages.info(
                request, 'Вам потрібно обрати рейтинг для цього товару')
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
    """ Функція зберігає відгук чи відповідь на відгук

    Args:
        request (_type_): запит
        pk (_type_): id товару
        answer (bool, optional): Це відповідь на відгук чи ні. Defaults to False.

    Returns:
        bool
    """
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
    """ Видаляє відгук

    Args:
        request (_type_): запит
        pk (_type_): id відгука

    Returns:
        bool
    """
    try:
        relation = Relation.objects.get(
            user_id=request.user.id, item_id=pk, pk=int(request.data.get('delete_relation')))
        relation.delete()
        set_rating(relation.item)
        return True
    except:
        return False
