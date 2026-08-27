from django import forms
from .models import User, Food, Category, Order, Comment


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Weka username', 'class': 'form-input', 'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Weka password', 'class': 'form-input'
    }))


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Weka username yako', 'class': 'form-input'
    }))
    answer = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'placeholder': 'Jibu swali la usalama', 'class': 'form-input'
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password mpya', 'class': 'form-input'
    }), min_length=6)


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'name_sw', 'category', 'price', 'icon', 'description',
                  'description_sw', 'image', 'image_url', 'rating', 'popular', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Chapati'}),
            'name_sw': forms.TextInput(attrs={'placeholder': 'e.g. Chapati'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'placeholder': 'e.g. 5000', 'min': 0}),
            'icon': forms.TextInput(attrs={'placeholder': 'e.g. 🍕', 'maxlength': 4}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe in English...', 'rows': 3}),
            'description_sw': forms.Textarea(attrs={'placeholder': 'Eleza kwa Kiswahili...', 'rows': 3}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.1}),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Weka password'
    }), min_length=6)

    class Meta:
        model = User
        fields = ['first_name', 'username', 'password', 'phone', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Jina Kamili'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'phone': forms.TextInput(attrs={'placeholder': 'e.g. 0712345678'}),
            'role': forms.Select(),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'phone']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password ya zamani'
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password mpya'
    }), min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Rudisha password mpya'
    }))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Jina lako', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email (optional)', 'class': 'form-input'}),
            'text': forms.Textarea(attrs={'placeholder': 'Maoni yako...', 'class': 'form-input', 'rows': 4}),
        }


class SettingsForm(forms.Form):
    whatsapp_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'placeholder': '255XXXXXXXXX', 'class': 'form-input'
    }))
