# Generated by Django 4.1.7 on 2023-03-26 22:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("partlibary", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="part",
            name="missing_in_db",
            field=models.BooleanField(default=False),
        ),
    ]
