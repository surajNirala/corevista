from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import random
import string
from django.conf import settings

class BlogCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.TextField(max_length=240,default="")
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table ='blog_categories'
    
    def __str__(self):
        return f'{self.user.username} - {self.name[:10]}'

class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory,on_delete=models.CASCADE)
    title = models.TextField(max_length=240,default="",unique=True)
    slug = models.SlugField(unique=True, blank=True)  # Slug field
    summary = models.TextField(max_length=1000, blank=True, null=True)
    description = models.TextField()
    photo = models.ImageField(upload_to='blogs/post/', blank=True, null=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table ='blogs'
    
    def save(self, *args, **kwargs):
        if not self.slug:  # If slug is empty, generate it
            generated_slug = slugify(self.title)
            # Ensure uniqueness by appending random string if slug already exists
            while Blog.objects.filter(slug=generated_slug).exists():
                generated_slug = slugify(self.title) + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            self.slug = generated_slug
        super().save(*args, **kwargs)
        
    
    def __str__(self):
        return f'{self.user.username} - {self.title[:10]} - {self.summary[:10]}'
