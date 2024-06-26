from django.db import models

    
class UserRole(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    OWNER = 'Owner', 'Owner'
    MANAGER = 'Manager', 'Manager'
    DRIVER = 'Driver', 'Driver'
    
class Category(models.TextChoices):
    SUV = "SUV", "SUV"
    Sedan = "Sedan", "Sedan"
    Truck = "Truck", "Truck"
    Jeep = "Jeep", "Jeep"
    Sports = "Sports", "Sports"

class Transmission(models.TextChoices):
    AUTOMATIC = 'A', 'Automatic'
    MANUAL = 'M', 'Manual'

class Fuel(models.TextChoices):
    GASOLINE = 'G', 'Gasoline'
    DIESEL = 'D', 'Diesel'
    ELECTRIC = 'E', 'Electric'
    
class VehicleStatus(models.TextChoices):
    APPROVED = "A", "Approved"
    REJECTED = "R", "Rejected"
    INREVIEW = "I", "In Review"
class CoverageType(models.TextChoices):
    COMPREHENSIVE = 'Comprehensive', 'Comprehensive'
    COLLISION = 'Collision', 'Collision'
    LIABILITY = 'Liability', 'Liability'
    # Add more coverage types as needed

class CoverageLimit(models.TextChoices):
    BODILY_INJURY = 'Bodily Injury', 'Bodily Injury'
    PROPERTY_DAMAGE = 'Property Damage', 'Property Damage'
    # Add more coverage limits as needed
