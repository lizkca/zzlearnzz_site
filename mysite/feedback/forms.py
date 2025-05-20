from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['type', 'title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }