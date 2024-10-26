from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class NewUserForm(UserCreationForm):
    mobile_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'focus:outline-none' , 'placeholder': '8976537692'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'focus:outline-none' , 'placeholder': 'user123'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'focus:outline-none'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'focus:outline-none'}))
    hostel_block = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'focus:outline-none' , 'placeholder': '2'}))
    room_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'focus:outline-none' , 'placeholder': '301'}))

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
            profile = Profile(
                user=user,
                mobile_number=self.cleaned_data['mobile_number'],
                hostel_block=self.cleaned_data['hostel_block'],
                room_number=self.cleaned_data['room_number']
            )
            profile.save()
        return user