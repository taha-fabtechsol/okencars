from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app import models


admin.site.register(models.User)
admin.site.register(models.Vehicle)
admin.site.register(models.VehicleImages)
# class UserAdmin1(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         (
#             "Additional Info",
#             {
#                 "fields": (
#                     "phone",
#                     "speciality",
#                     "image",
#                 ),
#             },
#         ),
#     )
#     list_display = (
#         "email",
#         "username",
#         "first_name",
#         "last_name",
#         "is_staff",
#         "is_superuser",
#     )
