from django.db.models import PositiveSmallIntegerField


class SkillValueField(PositiveSmallIntegerField):
    MAX_SKILL_VALUE = 100

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 0,
            'max_value': SkillValueField.MAX_SKILL_VALUE,
            **kwargs,
        })
