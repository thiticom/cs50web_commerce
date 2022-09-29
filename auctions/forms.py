from django import forms
from .models import Listing

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startbid','image', 'cat']