from django import forms
from .models import Profile, Camera, Location

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = "__all__"


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"
        exclude = ["creator"]


class SelectProfileForm(forms.Form):
    profile = forms.ModelChoiceField(queryset=Profile.objects.all())