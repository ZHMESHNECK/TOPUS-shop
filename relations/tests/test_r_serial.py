from relations.serializers import RelationSerializer
from relations.models import Relation
from products.models import Clothes
from users.models import User
from django.test import TestCase


class ClothSerializerTestCase(TestCase):
    def test_ok(self):
        """тест сериалайзера
        """
        user1 = User.objects.create(
            username='test1', is_staff=True, email='email1@email.email')
        user2 = User.objects.create(
            username='test2', is_staff=True, email='email2@email.email')

        item = Clothes.objects.create(
            title='da', price=250, s_code='', owner=user1, discount=20)
        item2 = Clothes.objects.create(
            title='net', price=550, s_code='da', owner=user2)

        Relation.objects.update_or_create(
            user=user1, item=item, rate=4, comment='text1', in_liked=True)
        Relation.objects.update_or_create(
            user=user2, item=item2, rate=5, comment='text2', in_liked=False)

        items = Relation.objects.all()
        data = RelationSerializer(items, many=True).data
        # print(data)
        # що чекаемо отримати, та що отримали
        expected_data = [
            {
                'item_id': item2.id,
                'rate': 5,
                'comment': 'text2',
                'parent': None,
                'in_liked': False,
            },
            {
                'item_id': item.id,
                'rate': 4,
                'comment': 'text1',
                'parent': None,
                'in_liked': True,
            },
        ]
        # print(expected_data)
        self.assertEqual(expected_data, data)
