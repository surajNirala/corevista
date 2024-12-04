# forms.py
from django import forms
from blog.models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'photo', 'summary', 'description','category']
    def clean_slug(self):
        # You can add custom validation for slug if necessary.
        return self.cleaned_data['slug']
