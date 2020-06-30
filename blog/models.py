from django.db import models
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Blogger(models.Model):
    """
    Stores a single blogger bio information, related to :model:'auth.User'.
    """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bio = models.CharField(max_length=300, verbose_name='Bio', help_text='Enter blogger biographical information')
   
    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])


class Post(models.Model):
    """
    Stores a single blog post, related to :model:'blog.Blogger'.
    """
    title = models.CharField(max_length=300, verbose_name='Title', help_text='Enter post title')
    blogger = models.ForeignKey('Blogger', on_delete=models.CASCADE, null=True)
    post_date = models.DateField(default=date.today(), verbose_name='Post date')
    content = models.TextField(max_length=5000, help_text='Enter post text', verbose_name='Description')

    class Meta:
        ordering = ['-post_date']
 
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])


class Comment(models.Model):
    """
    Stores a single comment, related to :model:'auth.User' and :model:'blog.Post'.
    """
    text = models.TextField(max_length=500, help_text='Enter comment', verbose_name='Description')
    post_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Post date')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return self.text
