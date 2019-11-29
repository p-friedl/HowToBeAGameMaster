from django.shortcuts import render
from django.views.generic import View

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
