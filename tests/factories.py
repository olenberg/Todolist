import factory.django
from factory import Faker
from core.models import User
from goals.models import Board, GoalCategory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'archi'
    first_name = 'Artur'
    last_name = 'Olenberg'
    email = 'olenberg.ai@yandex.ru'
    password = 'developer789!'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = Faker('test')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = Faker('test')
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
