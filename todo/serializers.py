from rest_framework import serializers
from django.contrib.auth.models import User


class TasksSerializers(serializers.Serializer):
    user_id = serializers.IntegerField()
    task=serializers.CharField(max_length=50)
    deadline=serializers.DateField()
    complete=serializers.BooleanField(default=False)
    incomplete=serializers.BooleanField(default=False)