from django.test import TestCase
from .models import  Image, Profile 
from django.contrib.auth.models import User

# Create your tests here.

class ImageTest(TestCase):
    def setUp(self):
        self.new_user = User(username='Michelle')
        self.new_user.save()
        self.new_profile = Profile(bio='test bio', owner=self.new_user, name='Michelle' )
        self.new_profile.save()
        self.new_image = Image(owner= self.new_profile, image_name='Nice Image', image_caption='Beautiful Description')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_image, Image))

    def test_save_method(self):
        self.new_image.save_image()
        images = Image.objects.all()
        self.assertTrue(len(images) > 0 )

    def test_delete_method(self):
        self.new_image.save_image()
        self.new_image.delete_image()
        images = Image.objects.all()
        self.assertTrue(len(images) == 0 )

    def test_update_caption(self):
        self.new_image.save_image()
        self.new_image.update_caption()
# Create your tests here.
