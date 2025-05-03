from django import forms

class SuperuserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username',
            'style': 'text-align: center;'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'style': 'text-align: center;'
        })
    )