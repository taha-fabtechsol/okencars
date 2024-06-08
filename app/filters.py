import django_filters
from django.db.models import Count, Q
from django.forms.widgets import TextInput
from django_filters import rest_framework as filters

from app import models


def placeholder(text):
    return TextInput(attrs={"placeholder": text})
