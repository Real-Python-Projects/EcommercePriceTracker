from django import forms


class ResetEmailForm(forms.Form):
    email = forms.EmailField()