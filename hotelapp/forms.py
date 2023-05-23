from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_name', 'description', 'image']
class ReservationForm(forms.ModelForm):
    start_date = forms.DateTimeField(
         widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    end_date = forms.DateTimeField(
         widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    class Meta:
        model = Reservation
        fields = ["username","room","start_date","end_date"]
class GuestReservationForm(forms.ModelForm):
    start_date = forms.DateTimeField(
         widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    end_date = forms.DateTimeField(
         widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    extra_services = forms.ModelMultipleChoiceField(queryset=ExtraService.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        model = Reservation
        fields = ["start_date","end_date","extra_services"]