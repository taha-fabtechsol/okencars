# Generated by Django 4.0.2 on 2024-06-08 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='insurance_expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='insurance_policy_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='insurance_provider',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]