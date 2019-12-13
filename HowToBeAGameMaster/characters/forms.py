from django.forms import modelform_factory, inlineformset_factory

from .models import Character, Skill


CharacterForm = modelform_factory(Character,
                                  fields=('kind', 'portrait', 'name', 'age', 'gender', 'appearance', 'religion',
                                          'profession', 'marital_status', 'player_notes'))

SkillFormSet = inlineformset_factory(Character,
                                     Skill,
                                     fields=('talent', 'name', 'value', 'include_talent_markup'),
                                     extra=1,
                                     max_num=80)
