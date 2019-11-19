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
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    appearance = models.CharField(max_length=500)
    religion = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
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



