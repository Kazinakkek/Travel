import os
from django.conf import settings
from datetime import datetime
from django.http import HttpRequest
from .forms import FeedbackForm, CommentForm, BookingForm, BlogForm
from .models import Tour, Comment, Booking
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse

def home(request):
    """Главная страница"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Страница контактов"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Наши контактные данные',
            'year':datetime.now().year,
        }
    )


def video_page(request):
    videos_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    os.makedirs(videos_dir, exist_ok=True)

    video_files = []
    for filename in os.listdir(videos_dir):
        file_path = os.path.join(videos_dir, filename)
        if os.path.isfile(file_path) and filename.lower().endswith('.mp4'):
            base_name = os.path.splitext(filename)[0]
            poster_filename = f"{base_name}_preview.jpg"
            poster_path = os.path.join(videos_dir, poster_filename)

            video_files.append({
                'title': base_name.replace('_', ' ').title(),
                'file': f'videos/{filename}',
                'poster': f'videos/{poster_filename}' if os.path.isfile(poster_path) else ''
            })

    return render(request, 'app/video.html', {
    'videos': video_files,
    'MEDIA_URL': settings.MEDIA_URL,
    'debug_info': {
        'media_root': settings.MEDIA_ROOT,
        'videos_dir': videos_dir,
        'files_found': os.listdir(videos_dir)
    }
})


@login_required
@user_passes_test(lambda u: u.is_staff)
def add_blog_post(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect('blogpost', pk=post.id)
    else:
        form = BlogForm()
    
    return render(request, 'app/add_blog_post.html', {'form': form})


@login_required
def book_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            booking.user = request.user
            booking.save()
            
            messages.success(request, 'Ваше бронирование успешно создано!')
            return redirect('booking_confirmation', pk=booking.pk)
    else:
        form = BookingForm()
    
    return render(request, 'tours/book_tour.html', {
        'tour': tour,
        'form': form
    })

def booking_confirmation(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'tours/booking_confirmation.html', {
        'booking': booking
    })


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # Проверяем, что пользователь - автор комментария или админ
    if request.user == comment.author or request.user.is_staff:
        comment.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('tour_detail', pk=comment.tour.pk)
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Недостаточно прав'}, status=403)
        return HttpResponseForbidden()

def tour_list(request):
    tours = Tour.objects.filter(is_active=True)
    return render(request, 'tours/tour_list.html', {'tours': tours})  # Изменили путь

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    comments = tour.comments.filter(active=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.tour = tour
            comment.author = request.user
            comment.save()
            return redirect('tour_detail', pk=tour.pk)
    else:
        form = CommentForm()
    
    return render(request, 'tours/tour_detail.html', {
        'tour': tour,
        'comments': comments,
        'form': form
    })

def about(request):
    """Страница о компании"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О компании',
            'message':'Информация о нашем турагентстве',
            'year':datetime.now().year,
        }
    )

def resources(request):
    """Страница полезных ресурсов"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/resources.html',
        {
            'title': 'Полезные ресурсы',
            'year': datetime.now().year,
        }
    )


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Получаем человекочитаемые значения
            rating_choices = dict(form.fields['rating'].choices)
            improvements_choices = dict(form.fields['improvements'].choices)
            visit_choices = dict(form.fields['visit_frequency'].choices)
            
            # Формируем данные для отображения
            data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'rating': rating_choices.get(form.cleaned_data['rating'], form.cleaned_data['rating']),
                'improvements': [improvements_choices.get(i, i) for i in form.cleaned_data['improvements']],
                'visit_frequency': visit_choices.get(form.cleaned_data['visit_frequency'], form.cleaned_data['visit_frequency']),
                'message': form.cleaned_data['message'],
            }
            return render(request, 'app/feedback_thanks.html', {'data': data})
    else:
        form = FeedbackForm()
    
    return render(request, 'app/feedback.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'app/registration.html', {
        'form': form,
        'title': 'Регистрация'
    })


