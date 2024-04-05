from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .serializers import ListSerializers
from rest_framework.decorators import api_view
from .models import Item
from rest_framework.response import Response
from django.contrib import messages
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

# lets display something using the funtion view
@login_required(login_url="/login-user")
@api_view(['GET'])
def TaskList(request):
 items = Item.objects.filter(user=request.user)
 serializers = ListSerializers(items, many=True).data
 return render(request, 'task_list.html', {'content':serializers})

@login_required(login_url="/login-user")
@api_view(['GET','POST'])
def editList(request, id):
 Extract=Item.objects.filter(user=request.user, id=id)
 serialized = ListSerializers(Extract, many=True).data
 if request.method == 'POST':
  new_title = request.POST['title']
  new_desc = request.POST['desc']
  Extract.update(title=new_title, description=new_desc)
  messages.success(request, 'You have successfully edited  {name} product'.format(name=request.user.username))
  return redirect('menu')
 return render(request, 'edit.html', {'content':serialized})

# now creating a delete function
@login_required(login_url='/login-user')
@api_view(['GET','POST'])
def viewdel(request, id):
 check = Item.objects.filter(user=request.user, id=id)
 if request.method=='POST' and check.exists():
  check.delete()
  messages.success(request,'you have successfully deleted the number {item} item in the list'.format(item=id))
  return redirect('menu')
 elif check == None:
  messages.error(request,'sorry the item you selected could be deleted')
 return render(request, 'delete.html')

@login_required(login_url="/login-user")
@api_view(['GET','POST'])
def detail(request, id):
 Item_detail = Item.objects.filter(user=request.user, id=id).values('id','title','description','create','complete').get()
 print(Item_detail['title'])
 return render(request, 'detail.html', {'content':Item_detail})

@login_required(login_url="/login-user")
@api_view(['GET','POST'])
def add_item(request):
 user = User.objects.get(pk=request.user.id)
 if request.method == 'POST':
  title = request.POST['title']
  describe= request.POST['describe']
  completed = request.POST['completed']
  new_item = Item.objects.create(user=user, title=title, description=describe, complete = completed)
  print(new_item)
  return redirect('menu')
 print(user)
 return render(request, 'create-items.html')

@api_view(['GET','POST'])
def login_user(request):
 if request.method == 'POST':
  usernm = request.POST['username']
  passcode = request.POST['password']
  print(usernm)
  auth_user = authenticate(request, username=usernm, password = passcode)
  if auth_user is not None:
   login(request, auth_user)
   messages.success(request,'{name} has successfully logged in'.format(name=request.user.username))
   return redirect('menu')
  else:
   messages.error(request,'invalid credentials')
 return render(request, 'login.html')

def logout_user(request):
 logout(request)
 messages.success(request,'{name} have successfully logged out'.format(name=request.user.username))
 return redirect('login-user')