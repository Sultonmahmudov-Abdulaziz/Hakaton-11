from django import forms
from.models import Comment

class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':4}))
    stars_given=forms.IntegerField(max_value=5,min_value=1)
    class Meta:
        model=Comment
        fields=('comment_text','stars_given')