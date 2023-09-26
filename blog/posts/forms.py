from django import forms 
from django.core.exceptions import ValidationError
from .models import (Post, User)
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Username is Required')
        if not User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Username does not exist')
        return username
    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        if not password:
            raise ValidationError('Password is required')
        user_obj = authenticate(username=username, password=password)
        if not user_obj:
            raise ValidationError('Credentials do not match')
        return password
        


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'password1', 'password2')
        
    def clean_username(self):
        super(UserRegistrationForm, self).clean()
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Username already esists')
        return username
    
    def clean_email(self):
        super(UserRegistrationForm, self).clean()
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user has already registered using this email')
        return email
    
    def clean_password2(self):
        super(UserRegistrationForm, self).clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 and not password2:
            raise ValidationError('Passwords is empty')
        if password1 != password2:
            raise ValidationError('Passwords must match')
        return password2
    

class PostForm(forms.ModelForm):
    # title = forms.CharField(max_length=255, required=True)
    # subject = forms.CharField(max_length=255, required=True)
    # description = forms.CharField()
    # main_image = forms.ImageField()
    
    class Meta:
        model = Post
        fields = ('title', 'subject', 'main_image', 'description')
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise ValidationError('Please add title')
        return title
    
    def clean_subject(self):
        subject = self.cleaned_data['subject']
        if not subject:
            raise ValidationError('Please add subject')
        return subject
    
    def clean_description(self):
        description = self.cleaned_data['description']
        if not description:
            raise ValidationError('Please add description')
        return description
    
    def clean_main_image(self):
        main_image = self.cleaned_data['main_image']
        if not main_image:
            raise ValidationError('Please add Image')
        return main_image