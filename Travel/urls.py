"""
Definition of urls for Travel.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from app import forms, views
from app.forms import RussianLoginForm
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('registration/', views.registration, name='registration'),
    path('login/', auth_views.LoginView.as_view(
        template_name='app/login.html',
        form_class=RussianLoginForm,
        extra_context={'title': 'Авторизация'}
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('resources/', views.resources, name='resources'),
    path('feedback/', views.feedback, name='feedback'),
    path('tours/', views.tour_list, name='tour_list'),
    path('tours/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('tour/book/<int:pk>/', views.book_tour, name='book_tour'),
    path('booking/confirmation/<int:pk>/', views.booking_confirmation, name='booking_confirmation'),
    path('blog/add/', views.add_blog_post, name='add_blog_post'),
    path('video/', views.video_page, name='video'),
]

# Обработка медиа-файлов (видео, картинки и т.д.) в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)