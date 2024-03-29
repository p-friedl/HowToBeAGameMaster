from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import CharacterForm, SkillFormSet


class Create(View):
    """
    Class representing the character create view
    """

    @method_decorator(login_required)
    def get(self, request):
        char_form = CharacterForm()
        skill_formset = SkillFormSet(prefix='skill')
        return render(request, 'characters/create.html', {'char_form': char_form, 'skill_formset': skill_formset})

    @method_decorator(login_required)
    def post(self, request):
        char_form = CharacterForm(request.POST)
        skill_formset = SkillFormSet(request.POST, prefix='skill')
        if char_form.is_valid() and skill_formset.is_valid():
            char_form.save(commit=False)
            char_form.instance.creator = request.user
            char_form.save()
            skill_formset.instance = char_form.instance
            skill_formset.save()
            return render(request, 'characters/create.html', {
                'text': request.POST['name']
            })

