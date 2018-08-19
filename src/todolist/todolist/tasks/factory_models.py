import factory
from todolist.users.factory_models import UserFactory
from .models import Task


class TaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = Task

    title = 'Novastone'
    description = 'Test'
    completed = False
    user = factory.SubFactory(UserFactory)