from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Character(models.Model):
    """
    Model for a How to be a Hero Pen & Paper Character
    """
    # choices
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

    # character relevant fields
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    shape = models.CharField(max_length=50)
    religion = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=2, choices=MARITAL_STATUS_CHOICES)
    portrait = models.ImageField()

    # game relevant fields
    talent_act, talent_knowledge, talent_social = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        editable=False
    )
    life_points = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        editable=False
    )
    rescue_points = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        editable=False
    )
