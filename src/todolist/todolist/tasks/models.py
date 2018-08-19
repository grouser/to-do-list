from django.db import models
from django.contrib.auth.models import User
from todolist.core.models import BaseModel


class Task(BaseModel):
    """
    Task that a user has to do
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.title, )