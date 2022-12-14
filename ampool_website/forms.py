from django import forms
from .models import CommentModel


class CommentForm(forms.ModelForm):
    at_blog = forms.CharField(widget=forms.HiddenInput())
    isreply = forms.CharField(widget=forms.HiddenInput())
    commentid = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = CommentModel
        fields = ['message', 'at_blog', 'isreply', 'commentid']