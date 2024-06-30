# Generated by Django 4.0.2 on 2024-06-30 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_vehicle_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='street_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='date_of_birth',
            new_name='dob',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='state_province',
            new_name='state',
        ),
        migrations.RemoveField(
            model_name='user',
            name='license_expiry_date',
        ),
        migrations.AlterField(
            model_name='user',
            name='dp',
            field=models.ImageField(default='/user-icon.png', upload_to='users_dp/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
