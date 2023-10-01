from django.db import models
from users.models import User
from django.urls import reverse
# https://pocoz.gitbooks.io/django-v-primerah/content/glava-7-sozdanie-internet-magazina/sozdanie-korzini/ispolzovanie-sessii-django.html
# https://evileg.com/ru/post/14/
# https://pocoz.gitbooks.io/django-v-primerah/content/glava-2-uluchshenie-bloga-s-pomoshyu-rasshirennyh-vozmozhnostej/sozdanie-sistemy-kommentariev.html

# https://www.youtube.com/watch?v=reFJ9hBLFUY


class Relation(models.Model):
    """Модель відношень
    """

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
        'products.MainModel', on_delete=models.CASCADE, verbose_name='об\'єкт', related_name='rati')
    rate = models.PositiveSmallIntegerField(
        'Оцінка', choices=RATING, default=0)
    in_liked = models.BooleanField('Обране', default=False)
    comment = models.TextField(
        'Коментарій', max_length=3000, null=True, blank=True)
    parent = models.ForeignKey(
        'self', verbose_name='parent', on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Зв'язок"
        verbose_name_plural = "Зв'язок"
        ordering = ['-created_at']
        

    def __str__(self) -> str:
        return f'{self.user.username} -> {self.item.title}'

    def __init__(self, *args, **kwargs):
        super(Relation, self).__init__(*args, **kwargs)
        self.old_rate = self.rate

    def save(self, *args, **kwargs):
        # При створенні зв'язку
        creating = not self.pk
        super().save(*args, **kwargs)
        if self.old_rate != self.rate or creating:
            from products.utils import set_rating
            set_rating(self.item)

    def get_absolute_url(self):
        return reverse('', kwargs={'id': self.id})