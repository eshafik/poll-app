from django import forms
from .models import Poll, Choice, Batch


class PollAddForm(forms.ModelForm):

    choice1 = forms.CharField(label='Choice 1', max_length=100, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice2 = forms.CharField(label='Choice 2', max_length=100, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    batch = forms.ModelChoiceField(queryset=Batch.objects.all().order_by('number'), required=True)

    class Meta:
        model = Poll
        fields = ['text', 'choice1', 'choice2', 'batch']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20})
        }


class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['text', 'batch']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', ]
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', })
        }
