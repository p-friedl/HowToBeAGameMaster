from django import forms

from .models import Character, Skill


class CharacterForm(forms.Form):
    """
    Class representing the character create form
    """
    kind = forms.CharField(widget=forms.Select(choices=Character.KIND_CHOICES), required=True)
    portrait = forms.ImageField(required=False)
    name = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(min_value=1, max_value=999, required=True)
    gender = forms.CharField(widget=forms.Select(choices=Character.GENDER_CHOICES), required=True)
    appearance = forms.CharField(max_length=500, required=True)
    religion = forms.CharField(max_length=100, required=True)
    profession = forms.CharField(max_length=100, required=True)
    marital_status = forms.CharField(widget=forms.Select(choices=Character.MARITAL_STATUS_CHOICES), required=True)
    player_notes = forms.CharField(widget=forms.Textarea, max_length=2000, required=False)


class SkillForm(forms.Form):
    """
    Class representing a skill creation form
    """
    skill_talent = forms.CharField(widget=forms.Select(choices=Skill.TALENT_CHOICE), required=True)
    skill_name = forms.CharField(max_length=50, required=True)
    skill_value = forms.IntegerField(min_value=1, max_value=100, required=True)

