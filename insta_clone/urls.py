from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('upload/', views.upload_images, name='upload'),
    path('delete/<str:pk>', views.delete_image, name='delete'),
    path('update/<str:pk>', views.update_image, name='update'),
    path('search', views.search, name='search'),
    
    path('profile/', views.profiles, name='profile'),  
    path('update_profile/<str:pk>', views.update_profile, name='update-profile'),
    path('comments/<str:pk>', views.comments, name='comments'),

    path('like/<str:pk>', views.like, name='likes'),
    path('follow/<str:pk>', views.follow, name='follow'),
    path('unfollow/<str:pk>', views.follow, name='unfollow'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

