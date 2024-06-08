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
    make = models.CharField(max_length=50,)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True)
    license_plate_number = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=5, choices=choices.Category.choices)
    number_of_seats = models.IntegerField()
    transmission_type = models.CharField(max_length=9, choices=choices.Transmission.choices)
    fuel_type = models.CharField(max_length=8, choices=choices.Fuel.choices)
    mileage = models.IntegerField()
    color = models.CharField(max_length=50)
    rental_price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    location_pickup = models.CharField(max_length=255)
    location_dropoff = models.CharField(max_length=255)
    availability_dates_from = models.DateField(null=True, blank=True)
    availability_dates_to = models.DateField(null=True, blank=True)
    additional_features = models.TextField(blank=True, null=True)
    
    # Insurance Information
    
    insurance_provider = models.CharField(max_length=255, null=True, blank=True)
    insurance_policy_number = models.CharField(max_length=255, null=True, blank=True)
    insurance_expiry_date = models.DateField(null=True, blank=True)
    coverage_type = models.CharField(max_length=13, choices=choices.CoverageType.choices)
    coverage_limits = models.CharField(max_length=15, choices=choices.CoverageLimit.choices)
    deductible_amount = models.PositiveIntegerField()
    roadside_assistance = models.BooleanField(default=False)
    rental_car_reimbursement = models.BooleanField(default=False)
    additional_insured_drivers = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

