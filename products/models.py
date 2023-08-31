from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Category(models.Model):
    """Модель  категорій
    """
    cat_name = models.CharField('Назва', max_length=100)
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")

    def __str__(self):
        return self.cat_name

    class Meta:
        verbose_name = 'Категорію'
        verbose_name_plural = 'Категорії'


class Gallery_cloth(models.Model):
    """Модель декількох фото "одягу" до 1-го об'єкту
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


class Rating(models.Model):
    RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.ForeignKey(
        'Clothes', on_delete=models.CASCADE, verbose_name='об\'єкт', related_name='cloth')

    class Meta:
        verbose_name = 'Руйтинг'
        verbose_name_plural = 'Рейтинг'


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


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.EmailField()
#     password = models.CharField()
#     image = models.ImageField(default='avatar.png', upload_to='profile/')
#     status = models.BooleanField(default=False)

#     def __str__(self):
#         return f'{self.user.username} Profile'

#     def save(self):
#         super().save()

#         img = Image.open(self.image.path)

#         if img.height > 300 or img.width > 300:
#             output_size = (300, 300)
#             img.thumbnail(output_size)
#             img.save(self.image.path)

#     class Meta:
#         verbose_name = 'Аккаунт'
#         verbose_name_plural = 'Аккаунти'


class MainModel(models.Model):
    title = models.CharField(max_length=150, verbose_name='Назва')
    description = models.TextField('Опис', blank=True, null=True)
    price = models.DecimalField('Вартість', max_digits=7, decimal_places=2)
    brand = models.CharField(max_length=50, verbose_name='Бренд', blank=True)
    main_image = models.ImageField(
        upload_to="main_photo", verbose_name='Фото', blank=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, verbose_name='Категорія')
    slug = models.SlugField(max_length=150, unique=True,
                            db_index=True, verbose_name='url')
    is_published = models.BooleanField(
        default=False, verbose_name='Публікація')


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

    size = models.CharField(max_length=2, choices=SIZE,
                            verbose_name='Розмір', null=True)
    season = models.CharField(
        max_length=11, choices=SEASON, null=True, verbose_name='Сезон')

    class Meta:
        verbose_name = 'Одяг'
        verbose_name_plural = 'Одяг'


class Gaming(MainModel):
    """Модель ігрової переферії
    """
    model = models.CharField(
        max_length=50, verbose_name='Модель', null=True)
    color = models.CharField(max_length=15, null=True, verbose_name='Колір')

    class Meta:
        verbose_name = 'Ігрова переферія'
        verbose_name_plural = 'Ігрова переферія'


class Home(MainModel):
    """Модель товарів для дому
    """
    material = models.CharField(max_length=50, null=True)
    color = models.CharField(max_length=15, null=True, verbose_name='Колір')
    Room_Type = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Для дому'
        verbose_name_plural = 'Для дому'
