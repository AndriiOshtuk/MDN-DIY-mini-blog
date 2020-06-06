from django.forms import ModelForm

from blog.models import Comment

class AddCommentModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']