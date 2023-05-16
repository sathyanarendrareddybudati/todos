from django.forms import ModelForm
from todo.models import Tasks
class Tasklist(ModelForm):  
    class Meta:
        model=Tasks
        fields=['task', 'incomplete', 'complete', 'deadline']