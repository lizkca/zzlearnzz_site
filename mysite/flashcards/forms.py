from django import forms
from .models import Flashcard

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['word', 'phonetic', 'definition', 'example_sentence']
        widgets = {
            'word': forms.TextInput(attrs={'class': 'form-control'}),
            'phonetic': forms.TextInput(attrs={'class': 'form-control'}),
            'definition': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'example_sentence': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'word': '单词',
            'phonetic': '音标',
            'definition': '定义',
            'example_sentence': '例句'
        }
