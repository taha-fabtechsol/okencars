from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from app import models


class NewUserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = [
            "email",
            "first_name",
            "last_name",
            "dp",
            "role",
            "phone_number",
            "street_address",
            "city",
            "state_province",
            "postal_code",
            "country",
            "date_of_birth",
            "license_number",
            "license_issuing_country",
            "license_expiry_date",
            "password",
        ]
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class VehicleForm(forms.ModelForm):
    class Meta:
        model = models.Vehicle
        exclude = ("owner",)