from django import forms


class LoginCreateForm(forms.Form):
    email = forms.EmailInput()
    phone_number = forms.CharField()
    password = forms.PasswordInput()

class LoginForm(forms.Form):
    email = forms.EmailInput()
    password = forms.PasswordInput()

    def authenticate(self):
        pass