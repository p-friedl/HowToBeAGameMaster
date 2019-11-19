from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Bin(models.Model):
    """
    Model for a Bin which serves as container for Items.
    Is the parent object for Character Inventories and other
    game relevant things which might contain Items.
    """

    # fields
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=20
    )
    capacity_validation = models.BooleanField(default=False)


class Item(models.Model):
    """
    Model for a How to be a Hero Pen & Paper Item.
    A Bin can contain n Items.
    """

    # choices
    KIND_CHOICES = [
        ('gp', 'general purpose'),
        ('w', 'weapon'),
        ('a', 'ammunition'),
        ('p', 'protection')
    ]

    # fields
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE)
    kind = models.CharField(max_length=2, choices=KIND_CHOICES)
    name = models.CharField(max_length=50)
    amount = models.PositiveSmallIntegerField()
    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
