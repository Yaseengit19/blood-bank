# Generated by Django 3.2.25 on 2025-03-02 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0003_auto_20250228_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='has_health_issues',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='donor',
            name='last_donation_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='donor',
            name='weight',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
