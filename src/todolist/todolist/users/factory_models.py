from django.contrib.auth.models import User
import factory


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'novastone'
    password = factory.PostGenerationMethodCall('set_password', 'test')
    is_active = True
