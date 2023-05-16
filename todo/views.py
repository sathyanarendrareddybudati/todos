from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from todo.forms import Tasklist
from .models import Tasks,Activity
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from todo.serializers import TasksSerializers


class TasksAPI(APIView):
    def get(self, request,pk=None):
        id=pk
        if id is not None:
            task=Tasks.objects.get(id=id)
            serializer=TasksSerializers(task)
            return Response(serializer.data)
        tasks=Tasks.objects.all()
        serializer=TasksSerializers(tasks,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = TasksSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        id=pk
        task = self.get_object(id=id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required(login_url='signin')
def home(request):
    if request.user.is_authenticated:
        user= request.user
        print(user)
        form=Tasklist()
        todos=Tasks.objects.filter(user=user,todo_status=True)
        return render(request , 'index.html' , context={'form' : form,'todos':todos})


def signin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            HttpResponse('creditional are wrong')
    return render(request,'signin.html')
    

def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        Email=request.POST.get('email')
        password=request.POST.get('password')
        my_user=User.objects.create_user(username=username,email=Email,password=password)
        my_user.save()
        return redirect('signin')    
    return render(request,'signup.html')

@login_required(login_url='signin')
def add_todo(request):
    if request.user.is_authenticated:
        user= request.user
        print(user)
        form = Tasklist(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)
            return redirect("home")
        else: 
            return render(request , 'index.html' , context={'form' : form})

@login_required
def delete_todo(request , id ):
    user_id=request.user
    print(id)
    todo=Tasks.objects.get(pk = id,user=user_id)

    if todo is not None:
        todo.todo_status=False
        todo.save()
    else:
        return HttpResponse("Task doesn't exist")
    Activity.objects.create(user=user_id,tasksId_id=todo.id,activity='d')
    return redirect('home')

@login_required
def todo_Edit(request,pk):
       user_id=request.user
       todo = Tasks.objects.get(id=pk,user=user_id)
       form=Tasklist(instance=todo) 
       Activity.objects.create(user=user_id,tasksId_id=todo.id,activity='e')
       if request.method == "POST":
              form=Tasklist(request.POST,instance=todo) 
              if form.is_valid():
                     form.save()
                     return redirect('home')
       
       return render(request, 'Edit.html',{'todo':todo,'updateform':form})

def change_todo(request , id  , status):
    todo = Tasks.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')


def User_Activity(request):
       user_id=request.user
       task=Activity.objects.all().filter(user=user_id)
       return render(request,'activity.html',{'todo':task})

@login_required
def signout(request):
    logout(request)
    return redirect('signin')
