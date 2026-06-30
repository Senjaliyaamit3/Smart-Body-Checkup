from django.db import models
from django.contrib.auth.models import User


class Prediction(models.Model):

    DISEASE_CHOICES = [
        ("Diabetes", "Diabetes"),
        ("Heart Disease", "Heart Disease"),
        ("Kidney Disease", "Kidney Disease"),
    ]

    RESULT_CHOICES = [
        ("Positive", "Positive"),
        ("Negative", "Negative"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="predictions"
    )

    disease = models.CharField(
        max_length=30,
        choices=DISEASE_CHOICES
    )

    result = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES
    )

    probability = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.disease}"