import random
from string import ascii_uppercase, digits
from products.models import MainModel


def serial_code_randomizer(args):
    """Генератор серійного номеру товару

    Args:
        args: category - Приймає категорію нової моделі

    Returns:
        str: Повертає рандомно згенеровану строку
    """
    if args == None:
        args = 0
    code_serial = str(args)+''.join(random.choice([*
                                                   ascii_uppercase, *digits]) for _ in range(9))
    find_copy = MainModel.objects.filter(s_code=code_serial).first()
    while find_copy is not None:
        code_serial = str(args.id)+''.join(random.choice([*
                                                          ascii_uppercase, *digits]) for _ in range(9))
        find_copy = MainModel.objects.filter(
            s_code=code_serial).first()
    return code_serial
