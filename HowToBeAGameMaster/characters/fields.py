from django.db.models.fields import PositiveSmallIntegerField


class SkillValueField(PositiveSmallIntegerField):
    MAX_SKILL_VALUE = 100

    def get_internal_type(self):
        return "SkillValueField"

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 0,
            'max_value': SkillValueField.MAX_SKILL_VALUE,
            **kwargs,
        })
