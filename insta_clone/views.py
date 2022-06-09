from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as authlogin,logout
from django.contrib.auth.decorators import login_required

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
         profile = Profile(username=request.user.username, owner=user)
         profile.save()
         print(profile)

      return redirect('login')
   context = {
      'form': register_form,
   }


   return render(request, 'insta_clone/register.html', context)


def logout(request):
   return redirect('login')

@login_required()
def home(request):
   images = Image.objects.all()
   profile = request.user
   profile_info = Profile.objects.all().filter(owner=profile)
   profiles = Profile.objects.all()

   context = {
      'images': images,
      'profile_info': profile_info,
      'profiles': profiles,
   }

   return render(request, 'insta_clone/index.html', context)





@login_required(login_url='')
def search(request):
    query = request.GET.get('q')
    if query:
        images = Image.objects.filter(
            Q(image_name__icontains=query) |
            Q(owner__name__icontains=query) |
            Q(image_caption__icontains=query)
        )
        context = {'images': images}
        return render(request, 'insta_clone/search.html', context)


@login_required(login_url='')
def upload_images(request):
    form = AddImageForm()
    user = request.user
    owner = Profile.objects.filter(owner=request.user).first() 
    print(owner)
    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_name = form.cleaned_data['image_name']
            image_caption = form.cleaned_data['image_caption']
            upload = Image(image=image, image_name=image_name,
                           image_caption=image_caption)
            upload.owner = owner
            upload.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'insta_clone/upload.html', context)


@login_required(login_url='')
def delete_image(request, pk):
    image = Image.objects.get(id=pk)
    if request.method == "POST":
        image.delete()
        return redirect('home')
    return render(request, 'insta_clone/delete.html', {'obj': image})


@login_required(login_url='')
def update_image(request, pk):
    image = Image.objects.get(id=pk)
    form = UpdateImageForm(request.POST or None, instance=image)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.owner = request.user.profile
            form.instance.image = image.image
            form.instance.image_name = image.image_name
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'insta_clone/update.html', context)


@login_required(login_url='')
def comments(request, pk):
    image = Image.objects.get(id=pk)
    comments = Comment.objects.filter(image=image)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        print(comment)
        comment_owner = Profile.objects.get(owner=request.user)
        new_comment = Comment.objects.create(
            comment=comment, image=image, owner=comment_owner)
        new_comment.save()

    context = {'comment': comments, 'image': image}
    return render(request, 'insta_clone/comments.html', context)


@login_required(login_url='')
def profiles(request):
    user = request.user
    profile = Profile.objects.get(owner=request.user)

    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()

    images = Image.objects.filter(owner=profile)
    context = {'profile': profile, 'images': images, 'following_count':following_count,'followers_count':followers_count,}
    return render(request, 'insta_clone/profile.html', context)


def update_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST,request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    form = UpdateProfileForm()
    context = {'form': form}
    return render(request, 'insta_clone/update.html', context)


def like(request, pk):
    user = request.user
    image = Image.objects.get(id=pk)
    current_likes = image.likes
    liked = Likes.objects.filter(user=user, image=image).count()

    if not liked:
            class_name = 'red'
            like = Likes.objects.create(user=user, image=image)
            current_likes = current_likes + 1

    else:
            Likes.objects.filter(user=user, image=image).delete()
            current_likes = current_likes - 1

    image.likes = current_likes
    image.save()

    return HttpResponseRedirect(reverse('home'))


def unfollow(request, pk):
    if request.method == 'GET':
        try:
            user_profile2 = User.objects.get(username=pk)
        except User.DoesNotExist:
            user_profile2 = None

        unfollow_d = Follow.objects.filter(follower=request.user, following=user_profile2)
        unfollow_d.delete()
        return redirect('profile')

def follow(request, pk):
    if request.method == 'GET':
        try:
            user_profile3 = User.objects.get(username=pk)
        except User.DoesNotExist:
            user_profile3 = None

        follow_s = Follow(follower=request.user, following=user_profile3)
        follow_s.save()
        return redirect('profile')