# Generated by Django 3.2.25 on 2025-02-28 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0008_auto_20250301_0245'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodrequest',
            name='last_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
