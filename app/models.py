from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from app import choices

class User(AbstractUser):
    owner = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    email = models.EmailField(_("Email"), unique=True, null=False)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    dp = models.ImageField(upload_to="users_dp/",)
    role = models.CharField(max_length=20, choices=choices.UserRole.choices, default=choices.UserRole.DRIVER)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state_province = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    license_issuing_country = models.CharField(max_length=100, blank=True, null=True)
    license_expiry_date = models.DateField(blank=True, null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    
class Vehicle(models.Model):
    owner = models.ForeignKey(User, verbose_name=_("User"), related_name="vehicles",on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    number = models.CharField(max_length=150)
    rent = models.FloatField()
    lic_number = models.CharField(max_length=150)
    res_id = models.CharField(max_length=150)
    year = models.IntegerField()
    make = models.CharField(max_length=150)
    model = models.CharField(max_length=150)
    fuel_type = models.CharField(max_length=1, choices=choices.Fuel.choices, default=choices.Fuel.DIESEL)
    transmission_type = models.CharField(max_length=1, choices=choices.Transmission.choices, default=choices.Transmission.MANUAL)
    mileage = models.IntegerField()
    status = models.CharField(choices=choices.VehicleStatus.choices, default=choices.VehicleStatus.INREVIEW, max_length=1)

class VehicleImages(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    image = models.FileField(upload_to="vehicle_images/")
