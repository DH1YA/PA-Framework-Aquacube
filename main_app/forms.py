from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, AgentApplication
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'first_name', 'email', 'phone']

    # Custom placeholder
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control item', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control item', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control item', 'placeholder': 'Confirm Password'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control item', 'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control item', 'placeholder': 'Email'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control item', 'placeholder': 'Phone Number'})

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'phone', 'profile_image']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control item',
            'placeholder': 'Username',
            'id': 'username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control item',
            'placeholder': 'Password',
            'id': 'password',
        })
    )
    
class PaymentForm(forms.Form):
    contact = forms.CharField(
        max_length=15,
        label='Phone Number',
        widget=forms.NumberInput(attrs={'class': 'form-control'}) 
    )
    payment_proof = forms.ImageField(
        label='Upload Payment Proof',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})  
    )

# forms.py
class AgentApplicationForm(forms.ModelForm):
    class Meta:
        model = AgentApplication
        fields = ['company_name', 'company_address', 'company_email', 'company_contact', 'npwp', 'photo']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            'company_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company address'
            }),
            'company_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company email'
            }),
            'company_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company contact number'
            }),
            'npwp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter NPWP number'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

class AgentChangeForm(UserChangeForm):
    class Meta:
        model = AgentApplication
        fields = ['company_name', 'company_address', 'npwp', 'photo', 'company_contact', 'company_email']