from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple


from .models import *


class AddAuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["born_date"].required = False
        self.fields["born_location"].required = False
        self.fields["description"].required = False

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]
        widgets = {
            "fullname": forms.TextInput(attrs={"class": "form-input"}),
            "born_date": forms.TextInput(
                attrs={
                    "class": "form-input",
                }
            ),
            "born_location": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(
                attrs={"cols": 60, "rows": 10},
            ),
        }


class AddTagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Tag
        fields = [
            "name",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
        }


class AddQuoteForm(forms.ModelForm):
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.SelectMultiple(),)  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["author"].empty_label = "Not selected"

    class Meta:
        model = Quote
        fields = ["tags", "author", "quote"]
        widgets = {
            "quote": forms.Textarea(attrs={"cols": 60, "rows": 10}),
        }
