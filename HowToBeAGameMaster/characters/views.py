from django.shortcuts import render
from django.views.generic import View

from .forms import CharacterForm


class Create(View):
    def get(self, request):
        form = CharacterForm
        return render(request, 'characters/create.html', {'form': form})

    def post(self, request):
        form = CharacterForm(request.POST)

        if form.is_valid():
            return render(request, 'characters/create.html', {
                'text': request.POST['name']
            })
