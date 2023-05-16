from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone

def validate(date):
    if date < timezone.now().date():
        raise ValidationError("date must be in present")

class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    task=models.CharField(max_length=50)
    deadline=models.DateField(validators=[validate])
    complete=models.BooleanField(default=False)
    incomplete=models.BooleanField(default=False)
    todo_status=models.BooleanField(default=True)

    def __str__(self):
        return self.task

    class Meta:
        ordering = ['complete']


class Activity(models.Model):
          user=models.ForeignKey(User, on_delete=models.CASCADE)
          tasksId=models.ForeignKey(Tasks, on_delete=models.CASCADE)
          activity_choices=[('a','add'),('e','edit'),('d','delete')]
          activity=models.CharField(max_length=50,choices=activity_choices)


          def _str_(self):
                    return self.user.email
