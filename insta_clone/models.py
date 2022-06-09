from django.db import models

# Create your models here.
class Profile(models.Model):
    username = models.CharField(max_length=40,blank=True)
    bio = models.TextField(max_length=300)
    prof_pic = models.ImageField(upload_to="profile/")

class Image(models.Model):
    image = models.ImageField(upload_to="image/",height_field=none,width_field=None,max_length=100)
    image_name = models.CharField(max_length=40)
    image_caption = models.TextField(max_length=500, blank=True)
    likes = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    comments = models.TextField()
    owner = models.ForeignKey(profile, on_delete=models.CASCADE)

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