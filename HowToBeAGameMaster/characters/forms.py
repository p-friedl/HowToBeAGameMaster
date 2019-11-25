from django import forms

from.models import Character


class CharacterForm(forms.Form):
    kind = forms.Select(choices=Character.KIND_CHOICES)
    name = forms.CharField(max_length=100)
    age = forms.IntegerField() # TODO: Valdiation logic research
    gender = forms.Select(choices=Character.GENDER_CHOICES)
    appearance = forms.CharField(max_length=500)
    religion = forms.CharField(max_length=100)
    profession = forms.CharField(max_length=100)
    marital_status = forms.Select(choices=Character.MARITAL_STATUS_CHOICES)
    player_notes = forms.CharField(widget=forms.Textarea, max_length=2000, required=False)
    portrait = forms.ImageField(required=False)
