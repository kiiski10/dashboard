from django import forms

class ProfileForm(forms.Form):
    profile_name = forms.CharField(label='Profile name', max_length=100)
