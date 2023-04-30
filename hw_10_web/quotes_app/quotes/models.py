from django.db import models
from django.urls import reverse
from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    Model,
    SlugField,
    TextField,
)
from django.utils.text import slugify


class Quote(Model):
    tags = ManyToManyField("Tag")
    author = ForeignKey(
        "Author",
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name="Author",
    )
    quote = TextField(blank=False)
    time_create = DateTimeField(auto_now_add=True, verbose_name="Created")
    time_update = DateTimeField(auto_now=True, verbose_name="Updated")
    is_published = BooleanField(default=True)

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
        ordering = ["-time_create"]


class Author(Model):
    fullname = CharField(max_length=100)
    born_date = CharField(
        max_length=50,
    )
    born_location = CharField(
        max_length=255,
    )
    description = TextField(
        blank=False,
        verbose_name="Description",
    )
    slug = SlugField(max_length=55, unique=True, db_index=True, verbose_name="URL")
    time_create = DateTimeField(auto_now_add=True, verbose_name="Created")
    time_update = DateTimeField(auto_now=True, verbose_name="Updated")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fullname)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("author", kwargs={"author_slug": self.slug})

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ["fullname"]


class Tag(Model):
    name = CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
