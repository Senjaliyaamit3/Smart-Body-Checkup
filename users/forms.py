from django import forms
from django.contrib.auth.models import User
from .models import Patient


class RegisterForm(forms.ModelForm):

    first_name = forms.CharField(max_length=100)
    last_name  = forms.CharField(max_length=100)
    username   = forms.CharField(max_length=100)
    email      = forms.EmailField()
    password   = forms.CharField(widget=forms.PasswordInput())
    age        = forms.IntegerField()
    gender     = forms.ChoiceField(choices=Patient.GENDER_CHOICES)
    phone      = forms.CharField(max_length=15)
    blood_group = forms.ChoiceField(choices=Patient.BLOOD_GROUPS)
    height     = forms.FloatField()
    weight     = forms.FloatField()
    address    = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))  # ← fix: explicit field

    class Meta:
        model  = Patient
        fields = ['age', 'gender', 'phone', 'blood_group', 'height', 'weight', 'address']