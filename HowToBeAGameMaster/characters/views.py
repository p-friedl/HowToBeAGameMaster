from django.shortcuts import render
from django.views.generic import View
from django.forms import modelformset_factory, inlineformset_factory

from .models import Character, Skill
from .forms import CharacterForm


class Create(View):
    """
    Class representing the character create view
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


class Createnew(View):
    """
    Class representing the character create view
    """
    CharacterFormSet = modelformset_factory(Character, fields=('kind', 'portrait', 'name', 'age', 'gender',
                                                               'appearance', 'religion', 'profession', 'marital_status',
                                                               'player_notes'))
    SkillFormSet = inlineformset_factory(Character, Skill)

    def get(self, request, CharacterFormSet=CharacterFormSet):
        char_form = CharacterFormSet()
        return render(request, 'characters/create_new.html', {'char_form': char_form})

    def post(self, request, CharacterFormSet=CharacterFormSet):
        char_form = CharacterFormSet(request.POST)

        if char_form.is_valid():
            char_form.save()
            return render(request, 'characters/create.html', {
                'text': request.POST['name']
            })
