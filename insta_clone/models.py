from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    username = models.CharField(max_length=40,blank=True)
    bio = models.TextField(max_length=300)
    prof_pic = models.ImageField(upload_to="profile/")
    owner = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile',)

class Image(models.Model):
    image = models.ImageField(upload_to="image/",height_field=None,width_field=None,max_length=100)
    image_name = models.CharField(max_length=40)
    image_caption = models.TextField(max_length=500, blank=True)
    likes = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.image_name

    def save_image(self):
        return self.save()

    def delete_image(self):
        return self.delete()

    def update_caption(self,pk):
        image_caption=self.objects.get(image_caption=pk)

        return image_caption.save()
    
    def count_likes(self):
        return self.likes.count()
    class Meta:
        ordering =['-date_created']

class Comment(models.Model):
    comment = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comment')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.comment

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='post_like')

    def user_liked_post(self, instance,*args,**kwargs):
        like = instance
        post = like.Post
        sender = like.User

    def user_unlike_post(self, instance,*args,**kwargs):
        like = instance
        post = like.Post
        sender = like.User

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def user_follow(sender, instance,*args,**kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following

    def user_unfollow(sender, instance,*args,**kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following
        