from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(null=False, max_length=255)
    subject = models.CharField(null=True, default='No subject', max_length=255)
    description = models.TextField(null=False)
    main_image = models.ImageField(upload_to='post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'post'
    
    def __str__(self):
        return f"{self.title} {self.created_at.strftime('%d-%m-%Y')}"
    
    