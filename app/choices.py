from django.db import models

    
class UserRole(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    OWNER = 'Owner', 'Owner'
    MANAGER = 'Manager', 'Manager'
    DRIVER = 'Driver', 'Driver'
    
class Category(models.TextChoices):
    SEDAN = 'Sedan', 'Sedan'
    SUV = 'SUV', 'SUV'
    TRUCK = 'Truck', 'Truck'
    # Add more categories as needed

class Transmission(models.TextChoices):
    AUTOMATIC = 'Automatic', 'Automatic'
    MANUAL = 'Manual', 'Manual'

class Fuel(models.TextChoices):
    GASOLINE = 'Gasoline', 'Gasoline'
    DIESEL = 'Diesel', 'Diesel'
    ELECTRIC = 'Electric', 'Electric'
    
class CoverageType(models.TextChoices):
    COMPREHENSIVE = 'Comprehensive', 'Comprehensive'
    COLLISION = 'Collision', 'Collision'
    LIABILITY = 'Liability', 'Liability'
    # Add more coverage types as needed

class CoverageLimit(models.TextChoices):
    BODILY_INJURY = 'Bodily Injury', 'Bodily Injury'
    PROPERTY_DAMAGE = 'Property Damage', 'Property Damage'
    # Add more coverage limits as needed
