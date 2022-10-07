from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()

    username.widget.attrs.update({
        'type': 'text',
        'name': 'txt',
        'placeholder': "User name",
        'required': '',
    })

    password = forms.CharField(widget=forms.PasswordInput)

    password.widget.attrs.update({
        'type': 'password',
        'name': 'pswd',
        'placeholder': "Password",
        'required': '',
    })

class RegistrationForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
