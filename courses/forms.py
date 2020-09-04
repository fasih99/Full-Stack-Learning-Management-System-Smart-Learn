from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module, Text


ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title', 'description'],
                                      extra=2,
                                      can_delete=True)
class TextForm(forms.Form):
     class Meta:
       model = Text, Course
       fields = ("__all__")

       widgets = {
     'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
     }


# This is the ModuleFormSet   formset. We build it using the
# inlineformset_factory()   function provided by Django.
#  Inline formsets are a small abstraction on top of formsets that simplify
#  working with related objects. This function allows us to build a model
#  formset dynamically for the Module objects related to a Course object.
