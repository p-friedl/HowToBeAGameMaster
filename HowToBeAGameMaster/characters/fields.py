from django.db.models import PositiveSmallIntegerField


class SkillValueField(PositiveSmallIntegerField):
    """
    custom field class for Skill Values
    sets a max_value of 100
    """
    MAX_SKILL_VALUE = 100

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 0,
            'max_value': SkillValueField.MAX_SKILL_VALUE,
            **kwargs,
        })
