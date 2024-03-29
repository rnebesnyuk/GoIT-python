# Generated by Django 4.2 on 2023-04-30 06:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quotes", "0003_alter_quote_options_alter_tag_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="quote",
            options={
                "ordering": ["-time_create"],
                "verbose_name": "Quote",
                "verbose_name_plural": "Quotes",
            },
        ),
        migrations.AlterField(
            model_name="author",
            name="description",
            field=models.TextField(verbose_name="Description"),
        ),
    ]
