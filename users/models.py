from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.PositiveIntegerField()

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    phone = models.CharField(max_length=15)

    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS)

    height = models.FloatField(help_text="Height in cm")

    weight = models.FloatField(help_text="Weight in kg")

    address = models.TextField()

    def __str__(self):
        return self.user.username