from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import (
    DateTimeField,
    EmbeddedDocumentField,
    ListField,
    StringField,
    ReferenceField,
)


class Tag(EmbeddedDocument):
    name = StringField()


class Author(Document):
    fullname = StringField()
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Author)
    quote = StringField()
    meta = {"allow_inheritance": True}
