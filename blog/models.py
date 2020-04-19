from django.db import models
from datetime import date
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

# Create your models here.
class Blogger(models.Model):
    nickname = models.CharField(max_length=50, help_text="Enter blogger nickname")
    bio = models.CharField(max_length=300, help_text="Enter blogger biographical information")

    #TODO How to connect with blogs list?
    # blogs_list = models.
   
    class Meta:
        ordering = ['nickname']
 
    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])

           
class Post(models.Model):
    title = models.CharField(max_length=100, help_text="Enter post title")
    blogger = models.ForeignKey('Blogger', on_delete=models.CASCADE, null=True)
    post_date = models.DateField(default=date.today())
    content = models.TextField(help_text="Enter post text")
    #TODO Add comments
    # comments = 

    class Meta:
        ordering = ['-post_date']
 
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

