from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # author = models.ForeignKey(User, on_delete='None')
    title = models.CharField(max_length=100)
    comlited = models.BooleanField(default=False)
    # description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
