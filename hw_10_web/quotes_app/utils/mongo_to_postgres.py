import os
import django

from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_app.settings")
django.setup()

from quotes.models import *


client = MongoClient("mongodb://localhost")

db = client.hw_10_web

authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author["fullname"],
        born_date=author["born_date"],
        born_location=author["born_location"],
        description=author["description"],
        slug=author["fullname"].replace(" ", "_").replace(".", "_").replace("'", "-"),
    )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote["tags"]:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    is_quote_exists = bool(len(Quote.objects.filter(quote=quote["quote"])))

    if not is_quote_exists:
        author = db.authors.find_one({"_id": quote["author"]})
        a = Author.objects.get(fullname=author["fullname"])
        q = Quote.objects.create(author=a, quote=quote["quote"])

        for tag in tags:
            q.tags.add(tag)
