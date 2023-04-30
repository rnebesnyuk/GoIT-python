from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

from .connect import get_mongodb
from .utils import *
from .models import *
from .forms import *


# Create your views here.


class QuotesHome(DataMixin, ListView):
    model = Quote
    template_name = "quotes/index.html"
    context_object_name = "quotes"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title="Main Page",
        )
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Quote.objects.filter(is_published=True).order_by("-time_create")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


class ShowAuthor(DataMixin, DetailView):
    model = Author
    template_name = "quotes/author.html"
    slug_url_kwarg = "author_slug"
    context_object_name = "author"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["author"])
        return dict(list(context.items()) + list(c_def.items()))


class AddAuthor(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddAuthorForm
    template_name = "quotes/addauthor.html"
    success_url = reverse_lazy("home")
    login_url = "/admin/"
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add Author")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        author = form.save()
        fullname = form.cleaned_data["fullname"]
        slug = slugify(fullname)
        messages.success(self.request, f"Author {fullname} was added!")
        return redirect("author", slug)


class AddTag(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddTagForm
    template_name = "quotes/addtag.html"
    success_url = reverse_lazy("home")
    login_url = "/admin/"
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add Tag")
        return dict(list(context.items()) + list(c_def.items()))


class AddQuote(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddQuoteForm
    template_name = "quotes/addquote.html"
    success_url = reverse_lazy("home")
    login_url = "/admin/"
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add Quote")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        quote = form.save()
        messages.success(self.request, f"Quote added!")
        return redirect(
            "home",
        )


class QuotesByTags(DataMixin, ListView):
    model = Quote
    template_name = "quotes/quotesbytag.html"
    context_object_name = "quotes"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Quotes by Tag", tag=self.kwargs["tag_id"])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Quote.objects.filter(tags__name=self.kwargs["tag_id"])
