from users.models import User
# from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """Модель  категорій
    """
    cat_name = models.CharField('Назва', max_length=100)
    slug = models.SlugField('URL', max_length=100, unique=True,
                            db_index=True)

    def __str__(self):
        return self.cat_name

    class Meta:
        verbose_name = 'Категорію'
        verbose_name_plural = 'Категорії'


class MainModel(models.Model):
    """Головна модель
    """
    title = models.CharField('Назва', max_length=150)
    description = models.TextField('Опис', blank=True)
    price = models.DecimalField('Вартість', max_digits=7, decimal_places=2)
    brand = models.CharField('Бренд', max_length=50, blank=True)
    main_image = models.ImageField('Фото',
                                   upload_to='main_photo', blank=True, null=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Категорія')
    s_code = models.CharField(
        'Код', max_length=10, unique=True, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name='Власник', related_name='create')
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='Час створення')
    discount = models.SmallIntegerField(
        default=0, verbose_name='Знижка')  # 0-100%
    is_published = models.BooleanField('Публікація',
                                       default=False)
    viewed = models.ManyToManyField(
        User, through='Rating', related_name='view')
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=None, null=True, verbose_name='Рейтинг')  # кэшуюче поле

    def __str__(self) -> str:
        return f'Id {self.id}: {self.title}'


class Clothes(MainModel):
    """Модель одягу
    """

    SIZE = (
        ('-', '-'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large')
    )
    SEASON = (
        ('ALL_SEASON', 'Все сезон'),
        ('SUMMER', 'Літо'),
        ('AUTUM', 'Осінь'),
        ('WINTER', 'Зима'),
        ('SPRING', 'Весна'),
    )

    DEPART = (
        ('Women', 'Жіноче'),
        ('Men', 'Чоловіче'),
        ('Unisex', 'Унісекс'),
    )

    size = models.CharField('Розмір', max_length=2, choices=SIZE, blank=True)
    season = models.CharField('Сезон', max_length=11,
                              choices=SEASON, blank=True)

    department = models.CharField('Стать', choices=DEPART, blank=True)

    class Meta:
        verbose_name = 'Одяг'
        verbose_name_plural = 'Одяг'


class Gaming(MainModel):
    """Модель ігрової переферії
    """
    material = models.CharField('Матеріал',
                                max_length=50, blank=True)
    model = models.CharField('Модель',
                             max_length=50, blank=True)
    color = models.CharField('Колір', max_length=15, blank=True)

    class Meta:
        verbose_name = 'Ігрова переферія'
        verbose_name_plural = 'Ігрова переферія'

    def __str__(self) -> str:
        return f'Id {self.id}: {self.title}'


class Home(MainModel):
    """Модель товарів для дому
    """
    material = models.CharField('Матеріал', max_length=50, blank=True)
    color = models.CharField('Колір', max_length=15, blank=True)
    room_type = models.CharField('Для кімнат', max_length=50, blank=True)
    weight = models.DecimalField(
        'Вага', max_digits=5, decimal_places=1, blank=True)
    dimensions = models.CharField('Розмір', max_length=30, blank=True)

    class Meta:
        verbose_name = 'Для дому'
        verbose_name_plural = 'Для дому'

    def __str__(self) -> str:
        return f'Id {self.id}: {self.title}'


class Rating(models.Model):
    """Модель рейтингу"""

    RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Юзер')
    item = models.ForeignKey(
        'MainModel', on_delete=models.CASCADE, verbose_name='об\'єкт', related_name='rati')
    rate = models.PositiveSmallIntegerField(
        'Оцінка', choices=RATING, null=True)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'

    def __str__(self) -> str:
        return f'{self.user.username}: {self.item.title} -> {self.rate}'

    def __init__(self, *args, **kwargs):
        super(Rating, self).__init__(*args, **kwargs)
        self.old_rate = self.rate

    def save(self, *args, **kwargs):
        # При створенні зв'язку
        creating = not self.pk
        super().save(*args, **kwargs)
        if self.old_rate != self.rate or creating:
            from products.utils import set_rating
            set_rating(self.item)


class Gallery_cloth(models.Model):
    """Модель декількох фото 'одягу' до 1-го об'єкту
    """
    images = models.ImageField('Фото', upload_to='cloth_photos')
    clothes_id = models.ForeignKey(
        'Clothes', verbose_name='cloth_photo', on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = 'Фото товару'
        verbose_name_plural = 'Фото товару'


class Gallery_gaming(models.Model):
    """Модель декількох фото "ігрової переферії" до 1-го об'єкту
    """
    images = models.ImageField('Фото', upload_to='gaming_photo')
    gaming_id = models.ForeignKey(
        'Gaming', verbose_name='gaming_photo', on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = 'Фото товару'
        verbose_name_plural = 'Фото товару'


class Gallery_home(models.Model):
    """Модель декількох фото категорії "для дому" до 1-го об'єкту
    """
    images = models.ImageField('Фото', upload_to='home_photo')
    home_id = models.ForeignKey(
        'Home', verbose_name='home_photo', on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = 'Фото товару'
        verbose_name_plural = 'Фото товару'


# https://www.youtube.com/watch?v=reFJ9hBLFUY
# class Review(models.Model):
#     email = models.EmailField()
#     name = models.CharField('логін', max_length=100)
#     text = models.TextField('текст', max_length=5000)
#     parent = models.ForeignKey(
#         'self', verbose_name="parent", on_delete=models.SET_NULL, blank=True, null=True
#     )

#     item = models.ForeignKey(
#         'Main_model', verbose_name='Об\'єкт', on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.email} - {self.name}'

#     class Meta:
#         verbose_name = 'Коментар'
#         verbose_name_plural = 'Коментарі'
