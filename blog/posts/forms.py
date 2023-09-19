from django import forms 
from django.core.exceptions import ValidationError
from .models import Post 

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