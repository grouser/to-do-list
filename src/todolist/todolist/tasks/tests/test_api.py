from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from todolist.users.factory_models import UserFactory
from todolist.tasks.models import Task
from todolist.tasks.factory_models import TaskFactory


class TaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(first_name='Novastone', last_name='Media', username='test', password='test')

    def test_check_permissions(self):
        """"Check that a user must be logged in and only see his tasks"""
        # User must be logged in
        resp = self.client.get(reverse('task-list'))
        self.assertEqual(resp.status_code, 403)
        task = TaskFactory()
        resp = self.client.get(reverse('task-detail', args=(task.pk,)))
        self.assertEqual(resp.status_code, 403)

    def test_task_list(self):
        """Check if a list of task is returned for the user that is logged in"""
        task1 = TaskFactory(user=self.user)
        task2 = TaskFactory(user=self.user, title='Task 2')
        self.client.login(username="test", password="test")
        resp = self.client.get(reverse('task-list'))
        self.assertEqual(resp.status_code, 200)
        # there are two tasks
        self.assertEqual(len(resp.data), 2)
        # check fields
        task = resp.data[0]
        fields = ["title", "description", "completed", "created", "modified"]
        for field in fields:
            self.assertIn(field, task)
        # Check the task1 is included
        self.assertEqual(task['title'], task1.title)

    def test_task_detail(self):
        """Check if we can retrieve a task"""
        task1 = TaskFactory(user=self.user)
        self.client.login(username='test', password='test')
        resp = self.client.get(reverse('task-detail', args=(task1.pk,)))
        self.assertEqual(resp.status_code, 200)
        task = resp.data
        fields = ["title", "description", "completed", "created", "modified"]
        for field in fields:
            self.assertIn(field, task)

    def test_task_create(self):
        """Check if a task is created for the user that is logged in"""
        self.client.login(username="test", password="test")
        data = {
            'title': 'Test Title',
            'description': 'This is a test.',
        }
        resp = self.client.post(reverse('task-list'), data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        created_task = resp.data
        self.assertEqual(created_task['title'], data['title'])
        # Check that current user has been set automatically in the new task
        task = Task.objects.get(pk=created_task['id'])
        self.assertEqual(task.user.username, 'test')

    def test_update_task(self):
        """Check that a user can update his tasks"""
        self.client.login(username="test", password="test")
        task = TaskFactory(user=self.user)
        data = {
            'title': 'Title Updated',
            'description': 'This is a test updated.',
        }
        resp = self.client.put(reverse('task-detail', args=(task.pk,)), data=data, content_type='application/json')
        task_updated = resp.data
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(task_updated['title'], data['title'])

    def test_user_cannot_update_other_user_tasks(self):
        """Check that a user cannot update other users' tasks"""
        self.client.login(username='test', password='test')
        task1 = TaskFactory(user=self.user)
        task2 = TaskFactory()
        data = {
            'title': 'Changed Title'
        }
        resp = self.client.patch(reverse('task-detail', args=(task2.pk,)), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 404)

    def test_delete_task(self):
        """Check that a task is updated successfully"""
        self.client.login(username="test", password="test")
        task = TaskFactory(user=self.user)
        resp = self.client.delete(reverse('task-detail', args=(task.pk,)))
        self.assertEqual(resp.status_code, 204)
        # Check that task does not exist
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=task.pk)

    def test_user_cannot_delete_other_users_tasks(self):
        """Check that a user cannot delete other users' tasks"""
        new_user = UserFactory()
        task = TaskFactory(user=new_user)
        self.client.login(username="test", password="test")
        resp = self.client.delete(reverse('task-detail', args=(task.pk,)))
        self.assertEqual(resp.status_code, 404)

    def test_set_task_as_completed(self):
        """Test that we can set a task as completed"""
        task = TaskFactory(user=self.user)
        self.client.login(username="test", password="test")
        data = {
            'completed': True
        }
        resp = self.client.patch(reverse('task-detail', args=(task.pk,)), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 200)