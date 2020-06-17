from django.db import models
from datetime import date
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User

# Create your models here.
class Blogger(models.Model):
    nickname = models.CharField(max_length=50, verbose_name='Nickname', help_text='Enter blogger nickname')
    bio = models.CharField(max_length=300, help_text='Enter blogger biographical information')

    #TODO How to connect with blogs list?
    # blogs_list = models.
   
    class Meta:
        ordering = ['nickname']

    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])


class Post(models.Model):
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
    text = models.TextField(max_length=500, help_text='Enter comment', verbose_name='Description')
    post_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Post date')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return self.text
