from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from items.models import Bin


class Character(models.Model):
    """
    Model for a How to be a Hero Pen & Paper Character.
    """

    # choices
    KIND_CHOICES = [
        ('PC', 'player character'),
        ('NPC', 'non-player character')
    ]
    GENDER_CHOICES = [
        ('M', 'male'),
        ('F', 'female'),
        ('O', 'other')
    ]
    MARITAL_STATUS_CHOICES = [
        ('single', 'single'),
        ('relationship', 'relationship'),
        ('married', 'married'),
        ('divorced', 'divorced'),
        ('widowed', 'widowed')
    ]

    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    # character relevant fields
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    appearance = models.CharField(max_length=500, default='')
    religion = models.CharField(max_length=100, default='')
    profession = models.CharField(max_length=100, default='')
    marital_status = models.CharField(max_length=15, choices=MARITAL_STATUS_CHOICES)
    player_notes = models.TextField(max_length=2000, blank=True, default='')
    game_master_notes = models.TextField(max_length=2000, blank=True, default='')
    portrait = models.ImageField(blank=True)

    # game relevant fields
    kind = models.CharField(
        max_length=3,
        choices=KIND_CHOICES,
    )
    talent_act = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        editable=False
    )
    talent_knowledge = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        editable=False
    )
    talent_social = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
        editable=False
    )
    life_points = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=100,
        editable=False
    )
    rescue_points = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0,
        editable=False
    )
    money = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

    def calculate_talents(self):
        """
        Method to calculate the three main talents: act, knowledge, social.
        Calculation is based on the Skill values related to talent:
        talent = summed Skill values related to the talent / 10
        Afterwards applies the talent value as a markup to the related Skills.
        Returns Diffs based on markups exceeding the Skill value limit of 100.
        """
        character = Character.objects.get(pk=self.pk)
        act, knowledge, social = 0, 0, 0
        # calc talent - skill value distribution
        for skill in character.skill_set.all():
            if skill.talent == 'act':
                act += skill.value
            elif skill.talent == 'knowledge':
                knowledge += skill.value
            else:
                social += skill.value
        # assign talent values
        self.talent_act = round(act / 10)
        self.talent_knowledge = round(knowledge / 10)
        self.talent_social = round(social / 10)
        self.save()

        # talent based skill markup
        diff_act, diff_knowledge, diff_social = 0, 0, 0
        for skill in character.skill_set.all():
            if skill.talent == 'act':
                diff_act += skill.add_talent_markup(self.talent_act)
            elif skill.talent == 'knowledge':
                diff_knowledge += skill.add_talent_markup(self.talent_knowledge)
            else:
                diff_social += skill.add_talent_markup(self.talent_social)
        return diff_act, diff_knowledge, diff_social

    def calculate_rescue_points(self):
        """
        Method to calculate the rescue_points.
        Calculation is based on the three main talent's values:
        rescue_points = (talent1 / 10) + (talent2) / 10 + (talent3) / 10
        """
        self.rescue_points = round(self.talent_act / 10) + \
                             round(self.talent_knowledge / 10) + \
                             round(self.talent_social / 10)
        self.save()


class Skill(models.Model):
    """
    Model for a How to be a Hero Pen & Paper Skill.
    A Character can have n Skills.
    """

    # choices
    TALENT_CHOICE = [
        ('act', 'act'),
        ('knowledge', 'knowledge'),
        ('social', 'social')
    ]

    # fields
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    talent = models.CharField(max_length=10, choices=TALENT_CHOICE)
    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def __str__(self):
        return self.name

    def add_talent_markup(self, markup):
        """
        Method to add the talent bonus markup for a skill.
        Called by the Character model's calculate_talents method.
        Returns a diff in case the markup exceeds the skill value limit of 100.
        """
        self.value += markup
        diff = 0
        if self.value > 100:
            diff = self.value - 100
            self.value = 100
        self.save()
        return diff


class Inventory(Bin):
    """
    Model for a How to be a Hero Pen & Paper Inventory. Inherits Bin.
    An Inventory can be associated to one Character only.
    """

    class Meta:
        verbose_name_plural = 'Inventories'

    # fields
    character = models.OneToOneField(
        Character,
        on_delete=models.CASCADE,
        primary_key=True
    )

    def __str__(self):
        return self.character.name
