from django.urls import path, include

from .views import *


urlpatterns = [
    path("", QuotesHome.as_view(), name="home"),
    path("add_tag/", AddTag.as_view(), name="add_tag"),
    path("add_author/", AddAuthor.as_view(), name="add_author"),
    path("add_quote", AddQuote.as_view(), name="add_quote"),
    path("author/<slug:author_slug>/", ShowAuthor.as_view(), name="author"),
    path("tag/<str:tag_id>/", QuotesByTags.as_view(), name="tag"),
]
