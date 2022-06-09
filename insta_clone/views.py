from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as authlogin

from .forms import RegisterForm, AddImageForm, UpdateImageForm,UpdateProfileForm
from insta_clone.models import Image,Profile,Follow,Likes,Comment

# Create your views here.
def login(request):
   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      print(username, password)

      try:
         user = User.objects.get(username=username, password=password)

      except:
         messages.error(request, 'Invalid username or password')

      user = authenticate(request, username=username, password=password)
      if user is not None:
         authlogin(request,user)
         return redirect('home')
      else:
         messages.error(request, 'Invalid username or password')

   return render(request, 'insta_clone/login.html')


def register(request):
   register_form = RegisterForm()
   if request.method == 'POST':
      form = RegisterForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.save()
         profile = Profile.objects.create(name=username , owner=user)
         profile.save()
         print(profile)

      return redirect('login')
   context = {
      'form': register_form,
   }

   return render(request, 'insta_clone/register.html', context)


def logout(request):
   return redirect('login')

      
