import random
from string import ascii_uppercase, digits
from products.models import MainModel
from relations.models import Relation
from django.db.models import Avg, Count


def gen_code(x: str) -> str:
    """Генератор серійних номерів

    Args:
         рандомні числа та букви
                    ↓
            (00)(00000000)
              ↑           
         category.id   

    Returns:
        str: серійний номер
    """
    return x.zfill(2)+(''.join(random.choice([*
                                              ascii_uppercase, *digits]) for _ in range(8)))


def serial_code_randomizer(args):
    """Генератор серійного номеру товару

    Args:
        args: category - Приймає категорію нової моделі

    Returns:
        str: Повертає рандомно згенеровану строку
    """
    if args == None:
        args = '0'
    else:
        args = str(args.id)
    code_serial = gen_code(args)
    find_copy = MainModel.objects.filter(s_code=code_serial).first()
    while find_copy is not None:
        code_serial = gen_code(args)
        find_copy = MainModel.objects.filter(
            s_code=code_serial).first()
    return code_serial


def set_rating(item):
    rating = Relation.objects.filter(item=item).aggregate(
        rating=Avg('rate')).get('rating')
    count = Relation.objects.filter(item=item).aggregate(
        count=Count('user')).get('count')
    item.rating = rating
    item.count = count
    item.save()
