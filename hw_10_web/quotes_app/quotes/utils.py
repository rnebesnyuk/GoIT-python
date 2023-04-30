from django.db.models import Count

from .models import *

menu = [
    {"title": "Home", "url_name": "home"},
    {"title": "Add Tag", "url_name": "add_tag"},
    {"title": "Add Author", "url_name": "add_author"},
    {"title": "Add Quote", "url_name": "add_quote"},
]


class DataMixin:
    paginate_by = 10

    def top10tags(self):
        top_tags = Tag.objects.annotate(num_quotes=Count("quote")).order_by(
            "-num_quotes"
        )[:10]
        tags_list = []
        for index, tag in enumerate(top_tags):
            tags_list.append({index: tag})
        return tags_list

    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
            user_menu.pop(1)
            user_menu.pop(1)

        context["menu"] = user_menu
        context["top_tags"] = self.top10tags()

        return context
