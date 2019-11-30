from django import forms

from .models import Character, Skill


class CharacterForm(forms.ModelForm):
    """
    Class representing a character create form with dynamic skills
    Inherits forms.ModelForm
    """
    class Meta:
        """
        Meta Class to define form model and fields
        """
        model = Character
        fields = ['kind', 'portrait', 'name', 'age', 'gender', 'appearance',
                  'religion', 'profession', 'marital_status', 'player_notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        skills = Skill.objects.filter(
            character=self.instance
        )
        for i in range(len(skills) + 1):
            skill_talent_field_name = 'skill_talent_{}'.format(i)
            skill_name_field_name = 'skill_name_{}'.format(i)
            skill_value_field_name = 'skill_value_{}'.format(i)
            self.fields[skill_talent_field_name] = forms.CharField(widget=forms.Select(choices=Skill.TALENT_CHOICE),
                                                                   required=True)
            self.fields[skill_name_field_name] = forms.CharField(max_length=50, required=True)
            self.fields[skill_value_field_name] = forms.IntegerField(min_value=1, max_value=100, required=True)

            try:
                self.initial[skill_talent_field_name] = skills[i].talent
                self.initial[skill_name_field_name] = skills[i].name
                self.initial[skill_value_field_name] = skills[i].value
            except IndexError:
                self.initial[skill_talent_field_name] = ""
                self.initial[skill_name_field_name] = ""
                self.initial[skill_value_field_name] = ""
                # create extra blank fields
                # TODO: evaluate if the below lines will be needed
                """
                skill_talent_field_name = 'skill_talent_{}'.format(i + 1)
                skill_name_field_name = 'skill_name_{}'.format(i + 1)
                skill_value_field_name = 'skill_value_{}'.format(i + 1)
                self.fields[skill_talent_field_name] = forms.CharField(widget=forms.Select(choices=Skill.TALENT_CHOICE),
                                                                       required=True)
                self.fields[skill_name_field_name] = forms.CharField(max_length=50, required=True)
                self.fields[skill_value_field_name] = forms.IntegerField(min_value=1, max_value=100, required=True)
                """

    def clean(self):
        skills = {
            'skill_talents': [],
            'skill_names': [],
            'skill_values': []
        }
        i = 0
        skill_name_field_name = 'skill_name_{}'.format(i)

        while self.cleaned_data.get(skill_name_field_name):
            skill_talent_field_name = 'skill_talent_{}'.format(i)
            skill_value_field_name = 'skill_value_{}'.format(i)

            skill_talent = self.cleaned_data[skill_talent_field_name]
            skill_name = self.cleaned_data[skill_name_field_name]
            skill_value = self.cleaned_data[skill_value_field_name]

            if skill_name in skills['skill_names']:
                self.add_error(skill_name_field_name, 'Duplicate')
            else:
                skills['skill_talents'].append(skill_talent)
                skills['skill_names'].append(skill_name)
                skills['skill_values'].append(skill_value)

            i += 1
            skill_name_field_name = 'skill_name_{}'.format(i)

        self.cleaned_data['skills'] = skills

    def save(self, commit=True):
        character = self.instance
        character.kind = self.cleaned_data['kind']
        character.portrait = self.cleaned_data['portrait']
        character.name = self.cleaned_data['name']
        character.age = self.cleaned_data['age']
        character.gender = self.cleaned_data['gender']
        character.appearance = self.cleaned_data['appearance']
        character.religion = self.cleaned_data['religion']
        character.profession = self.cleaned_data['profession']
        character.marital_status = self.cleaned_data['marital_status']
        character.player_notes = self.cleaned_data['player_notes']
        character.skill_set.all().delete()
        character.save()
        for i in range(len(self.cleaned_data['skills']['skill_names'])):
            Skill.objects.create(
                character=character,
                talent=self.cleaned_data['skills']['skill_talents'][i],
                name=self.cleaned_data['skills']['skill_names'][i],
                value=self.cleaned_data['skills']['skill_values'][i]
            )

    def get_skill_fields(self):
        for skill_field in self.fields:
            if skill_field.startswith('skill_talent_') or skill_field.startswith('skill_name_') \
                   or skill_field.startswith('skill_value_'):
                yield self[skill_field]



