# Generated by Django 4.2 on 2023-04-28 13:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("quotes", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="quote",
            options={
                "ordering": ["id"],
                "verbose_name": "Quote",
                "verbose_name_plural": "Quotes",
            },
        ),
    ]
