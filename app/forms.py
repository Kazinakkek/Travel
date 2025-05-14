from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.validators import MinLengthValidator
from .models import Comment, Booking, Blog


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class RussianLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['persons', 'notes']
        widgets = {
            'persons': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ваши пожелания...'
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Оставьте ваш комментарий...'
            }),
        }

class FeedbackForm(forms.Form):
    RATING_CHOICES = [
        (5, 'Отлично'),
        (4, 'Хорошо'),
        (3, 'Удовлетворительно'),
        (2, 'Плохо'),
        (1, 'Очень плохо'),
    ]

    name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    rating = forms.ChoiceField(
        label='Общая оценка сайта',
        choices=RATING_CHOICES,
        widget=forms.RadioSelect()
    )
    
    improvements = forms.MultipleChoiceField(
        label='Что можно улучшить? (выберите несколько вариантов)',
        choices=[
            ('design', 'Дизайн сайта'),
            ('content', 'Контент'),
            ('navigation', 'Навигация'),
            ('speed', 'Скорость работы'),
        ],
        widget=forms.CheckboxSelectMultiple()
    )
    
    visit_frequency = forms.ChoiceField(
        label='Как часто вы посещаете наш сайт?',
        choices=[
            ('daily', 'Ежедневно'),
            ('weekly', 'Еженедельно'),
            ('monthly', 'Ежемесячно'),
            ('first', 'Впервые'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    message = forms.CharField(
        label='Ваши пожелания',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4
        }),
        validators=[MinLengthValidator(10)]
    )

