from django.db import models

class Todolist(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=2048)
    completed = models.BooleanField(default=False,blank=False)
def __str__(self):
        return self.title
