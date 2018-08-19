from django.test import TestCase
from todolist.tasks.models import Task


class TestTaskModel(TestCase):
    def test_str_method(self):
        self.assertEqual(str(Task(title='Test')), 'Test')