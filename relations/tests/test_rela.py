from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from relations.models import Relation
from products.models import Clothes, Category
import json


class RelationTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create(
            username='user1', email='email1@email.email', is_staff=True)
        self.user2 = User.objects.create(
            username='user2', email='email2@email.email')
        self.user3 = User.objects.create(
            username='user3', email='email3@email.email')
        self.item = Clothes.objects.create(
            title='item1', price='150.00', s_code='1', size='S', season='SUMMER', owner=self.user)
        self.item2 = Clothes.objects.create(
            title='item2', price='100.00', s_code='2', size='S', season='test1')

        self.cat = Category.objects.create(cat_name='1', slug='1')
        self.cat2 = Category.objects.create(cat_name='2', slug='2')

        self.rel1 = Relation.objects.create(
            user=self.user, item=self.item, comment='us-it1', rate=5)
        self.rel2 = Relation.objects.create(
            user=self.user2, item=self.item2, comment='us2-it2', rate=5)
        self.rel3 = Relation.objects.create(
            user=self.user3, item=self.item2, comment='us3-it2', rate=5)

    def test_check_unique(self):
        """Тест на створення відгуку
        """
        url = reverse('cloth-detail', args=(self.item.id,))
        relations = Relation.objects.filter(item_id=self.item)
        self.assertEqual(1, len(relations))

        data = {
            'rate': 3,
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user2)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        relations = Relation.objects.filter(item_id=self.item)
        self.assertEqual(2, len(relations))

    def test_rate(self):
        """Змінення рейтингу
        """
        url = reverse('cloth-detail', args=(self.item.id,))

        relations = Relation.objects.filter(item=self.item)

        self.assertEqual(len(relations), 1)
        data = {
            'rate': 2,
            'confirm': True
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        relation = Relation.objects.get(user=self.user, item=self.item)
        self.assertEqual(relation.rate, 2)
        self.assertEqual(len(relations), 1)

    def test_rate_wrong(self):
        """Ставлення невірного рейтингу
        """
        url = reverse('cloth-detail', args=(self.item.id,))

        data = {
            'rate': 6,
            'confirm': True
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user)
        response = self.client.post(
            url, data=json_data, content_type='application/json')

        relation = Relation.objects.get(user=self.user, item_id=self.item)
        self.assertEqual(5, relation.rate)

    def test_staff_make_rel(self):
        """ staff дає відповідь на відгук
        """
        url = reverse('cloth-detail', args=(self.item.id,))
        review = Relation.objects.get(
            user=self.user2, item=self.item2)

        data = {
            'parent': review.id,
            'comment': 'Дякуємо за відгук'
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user)
        response = self.client.post(
            url, data=json_data, content_type='application/json')
        relation = Relation.objects.get(
            user=self.user, item_id=self.item, parent__isnull=False)

        self.assertEqual(relation.comment, 'Дякуємо за відгук')
        self.assertEqual(relation.parent, review)

    def test_user_make_rel_without_permiss(self):
        """ Юзер без прав дає відповідь на відгук
        """
        url = reverse('cloth-detail', args=(self.item.id,))
        review = Relation.objects.get(
            user=self.user, item=self.item)

        data = {
            'parent': review.id,
            'comment': 'Дякуємо за відгук'
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user2)
        response = self.client.post(
            url, data=json_data, content_type='application/json')

        relation = Relation.objects.filter(
            user=self.user, item_id=self.item, parent__isnull=False)

        self.assertEqual(0, len(relation))

    def test_delete_relation(self):
        """ Видалення юзером свого відгуку
        """

        url = reverse('cloth-detail', args=(self.item.id,))

        review = Relation.objects.filter(item_id=self.item.id)
        self.assertEqual(1, len(review))

        data = {
            'delete_relation': self.rel1.id,
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user)
        response = self.client.post(
            url, data=json_data, content_type='application/json')

        review = Relation.objects.filter(item_id=self.item.id)

        self.assertEqual(0, len(review))

    def test_staff_delete_relation(self):
        """ Видалення staff`oм своєї відповіді
        """

        url = reverse('cloth-detail', args=(self.item2.id,))

        answer = Relation.objects.create(
            item=self.item2, user=self.user, comment='Дякуємо', parent_id=self.rel2.id
        )
        review = Relation.objects.filter(item=self.item2)
        self.assertEqual(3, len(review))
        self.assertEqual(answer.parent_id, self.rel2.id)

        data = {
            'delete_relation': answer.id,
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user)
        response = self.client.post(
            url, data=json_data, content_type='application/json')

        review = Relation.objects.filter(item_id=self.item2.id)
        self.assertEqual('us2-it2', review[1].comment)
        self.assertEqual(2, len(review))

    def test_user_delete_relation_with_2_answers(self):
        """ Відалення відгуку с 2-ма відповідями
           видалення каскадне
        """

        url = reverse('cloth-detail', args=(self.item2.id,))

        Relation.objects.create(
            item=self.item2, user=self.user, comment='Дякуємо', parent_id=self.rel2.id
        )
        Relation.objects.create(
            item=self.item2, user=self.user, comment='Дякуємо 2', parent_id=self.rel2.id
        )
        review = Relation.objects.filter(item=self.item2)
        self.assertEqual(4, len(review))

        data = {
            'delete_relation': self.rel2.id,
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.user2)

        response = self.client.post(
            url, data=json_data, content_type='application/json')

        review = Relation.objects.filter(item_id=self.item2.id)
        self.assertEqual(1, len(review))

    def test_rate_after_delete_rel(self):
        """ Оновлення рейтингу після видалення відгуку с рейтингом 1
        """

        url = reverse('cloth-detail', args=(self.item2.id,))

        review = Clothes.objects.get(pk=self.item2.id)
        self.assertEqual(5, review.rating)

        relation = Relation.objects.create(
            user=self.user, item=self.item2, rate=1)

        review.refresh_from_db()
        self.assertEqual('3.7', str(review.rating))

        data = {
            'delete_relation': relation.id,
        }

        json_data = json.dumps(data)
        self.client.force_authenticate(self.user)
        response = self.client.post(
            url, data=json_data, content_type='application/json')

        review.refresh_from_db()
        self.assertEqual('5.0', str(review.rating))

    def test_in_fav(self):
        """ Додання до улюбленого
        """
        url = reverse('add_to_fav', args=(self.item.id,))
        item = self.item
        self.assertFalse(item.in_liked.filter(pk=self.user.id).exists())
        self.client.force_login(self.user)

        response = self.client.post(
            url, content_type='application/json')

        item.refresh_from_db()
        self.assertTrue(response.data['data'])
        self.assertTrue(item.in_liked.filter(pk=self.user.id).exists())

    def test_delete_from_fav(self):
        """ Видалення з улюбленого
        """
        url = reverse('add_to_fav', args=(self.item.id,))
        item = self.item
        self.assertFalse(item.in_liked.filter(pk=self.user.id).exists())
        self.client.force_login(self.user)

        response = self.client.post(
            url, content_type='application/json')
        self.assertTrue(response.data['data'])
        self.assertTrue(item.in_liked.filter(pk=self.user.id).exists())
        response = self.client.post(
            url, content_type='application/json')

        item.refresh_from_db()
        self.assertFalse(response.data['data'])
        self.assertFalse(item.in_liked.filter(pk=self.user.id).exists())
