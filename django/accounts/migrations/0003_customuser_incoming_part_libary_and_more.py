# Generated by Django 4.1.7 on 2023-03-24 05:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("partlibary", "0001_initial"),
        ("accounts", "0002_customuser_part_libary"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="incoming_part_libary",
            field=models.ManyToManyField(related_name="incoming", to="partlibary.part"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="old_part_libary",
            field=models.ManyToManyField(related_name="rollback", to="partlibary.part"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="part_libary",
            field=models.ManyToManyField(
                related_name="part_library", to="partlibary.part"
            ),
        ),
    ]
