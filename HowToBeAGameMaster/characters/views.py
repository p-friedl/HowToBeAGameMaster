from django.shortcuts import render
from django.views.generic import View

from .models import Character, Skill
from .forms import CharacterForm, SkillFormSet

"""
class Create(View):
    """
# Class representing the character create view
"""
    def get(self, request):
        char_form = CharacterForm
        return render(request, 'characters/create.html', {'char_form': char_form})

    def post(self, request):
        char_form = CharacterForm(request.POST)

        if char_form.is_valid():
            # TODO: implement authentication to be able to reimplement Character creator relation
            char_form.save()
            return render(request, 'characters/create.html', {
                'text': request.POST['name']
            })
"""
# TODO: refactor based on successful formset experiment
class Createnew(View):
    """
    Class representing the character create view
    """

    def get(self, request):
        char_form = CharacterForm()
        skill_formset = SkillFormSet()
        return render(request, 'characters/create_new.html', {'char_form': char_form, 'skill_formset': skill_formset})

    def post(self, request):
        char_form = CharacterForm(request.POST)
        skill_formset = SkillFormSet(request.POST)
        if char_form.is_valid() and skill_formset.is_valid():
            char_form.save()
            skill_formset.instance = char_form.instance
            skill_formset.save()
            return render(request, 'characters/create_new.html', {
                'text': request.POST['name']
            })
