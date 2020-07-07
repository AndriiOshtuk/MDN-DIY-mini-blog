from django.test import SimpleTestCase

from blog.forms import AddCommentModelForm


class AddCommentModelFormTest(SimpleTestCase):
    def test_renew_form_date_field_label(self):
        form = AddCommentModelForm()
        self.assertTrue(form.fields['text'].label == None or form.fields['text'].label == 'Description')

    def test_text_field_help_text(self):
        form = AddCommentModelForm()
        self.assertEqual(form.fields['text'].help_text, 'Enter comment comment about blog here.')
