# Generated by Django 3.2.25 on 2025-02-28 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_auto_20250228_1140'),
        ('blood', '0005_auto_20250228_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodrequest',
            name='request_by_hospital',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hospital.hospital'),
            preserve_default=False,
        ),
    ]
