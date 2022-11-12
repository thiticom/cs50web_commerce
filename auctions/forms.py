from tkinter import Widget
from django import forms
from .models import Listing, Comment, Bid

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startbid','image', 'cat']


class CloseForm(forms.ModelForm):
    temp_id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Listing
        fields = ['id', 'won_by', 'closed']
        widgets = {'id': forms.HiddenInput,
        'won_by': forms.HiddenInput,
        'closed': forms.HiddenInput}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'user', 'listing']
        widgets = {'user': forms.HiddenInput,
        'listing': forms.HiddenInput}


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid', 'user', 'listing']
        widgets = {'user': forms.HiddenInput,
        'listing': forms.HiddenInput}