from django.forms import ModelForm
from blog.models import Comment


class AddCommentModelForm(ModelForm):
    """
    Form to create instance of :model:'blog.Comment'

    **Template:**
    :template:'blog/comment_form.html'

    """
    class Meta:
        model = Comment
        fields = ['text']
