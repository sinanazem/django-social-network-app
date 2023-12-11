from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-'}))
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField()
    email = forms.EmailField()
    