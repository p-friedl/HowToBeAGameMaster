from django.shortcuts import render
from django.views.generic import View

from .forms import CharacterForm, SkillForm


class Create(View):
    """
    Class representing the character create view
    """
    def get(self, request):
        char_form = CharacterForm
        skill_form = SkillForm
        return render(request, 'characters/create.html',
                      {'char_form': char_form, 'skill_form': skill_form})

    def post(self, request):
        char_form = CharacterForm(request.POST)
        skill_form = SkillForm(request.POST)

        if char_form.is_valid() and skill_form.is_valid():
            return render(request, 'characters/create.html', {
                'text': request.POST['name']
            })
