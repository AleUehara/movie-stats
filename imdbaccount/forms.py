from django import forms
from imdbaccount.models import IMDBAccount

class IMDBAccountForm(forms.ModelForm):
    class Meta:
        model = IMDBAccount