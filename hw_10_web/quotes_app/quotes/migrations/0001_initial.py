# Generated by Django 4.2 on 2023-04-28 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fullname", models.CharField(max_length=100)),
                ("born_date", models.CharField(max_length=50)),
                ("born_location", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "slug",
                    models.SlugField(max_length=55, unique=True, verbose_name="URL"),
                ),
                (
                    "time_create",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "time_update",
                    models.DateTimeField(auto_now=True, verbose_name="Updated"),
                ),
            ],
            options={
                "verbose_name": "Author",
                "verbose_name_plural": "Authors",
                "ordering": ["fullname"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Quote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quote", models.TextField()),
                (
                    "time_create",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "time_update",
                    models.DateTimeField(auto_now=True, verbose_name="Updated"),
                ),
                ("is_published", models.BooleanField(default=True)),
                (
                    "author",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="quotes.author",
                        verbose_name="Author",
                    ),
                ),
                ("tags", models.ManyToManyField(to="quotes.tag")),
            ],
            options={
                "verbose_name": "Quote",
                "verbose_name_plural": "Quotes",
                "ordering": ["author"],
            },
        ),
    ]