import json
from datetime import datetime

from mongoengine import connect
from models import Author, Quote, Tag

import connect

with open("authors.json", "r", encoding="utf-8") as f:
    authors_data = json.load(f)

with open("quotes.json", "r", encoding="utf-8") as f:
    quotes_data = json.load(f)

for author_data in authors_data:
    born_data = datetime.strptime(author_data.pop("born_date"), "%B %d, %Y")
    author = Author(born_date=born_data, **author_data)
    author.save()

for quote_data in quotes_data:
    tags_data = quote_data.pop("tags")
    tags = [Tag(name=tag_data) for tag_data in tags_data]
    author_name = quote_data.pop("author")
    author = Author.objects.get(fullname=author_name)
    quote = Quote(tags=tags, author=author, **quote_data)
    quote.save()
