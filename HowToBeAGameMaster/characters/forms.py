from django import forms

from .models import Character


class CharacterForm(forms.Form):
    kind = forms.CharField(widget=forms.Select(choices=Character.KIND_CHOICES), required=True)
    name = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(min_value=1, max_value=999, required=True)
    gender = forms.CharField(widget=forms.Select(choices=Character.GENDER_CHOICES), required=True)
    appearance = forms.CharField(max_length=500, required=True)
    religion = forms.CharField(max_length=100, required=True)
    profession = forms.CharField(max_length=100, required=True)
    marital_status = forms.CharField(widget=forms.Select(choices=Character.MARITAL_STATUS_CHOICES), required=True)
    player_notes = forms.CharField(widget=forms.Textarea, max_length=2000, required=False)
    portrait = forms.ImageField(required=False)
# TODO next: implement skills