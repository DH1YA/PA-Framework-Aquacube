from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'first_name', 'email', 'phone', 'user_type']

    # Custom placeholder
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control item', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control item', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control item', 'placeholder': 'Confirm Password'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control item', 'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control item', 'placeholder': 'Email'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control item', 'placeholder': 'Phone Number'})
        self.fields['user_type'].widget.attrs.update({'class': 'form-control item'})

        # Optional: Custom labels
        for field in self.fields:
            self.fields[field].label = ''

