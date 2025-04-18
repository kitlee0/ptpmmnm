from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nhập mật khẩu'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Xác nhận mật khẩu'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Nhập số điện thoại'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Mật khẩu xác nhận không khớp!")

        return cleaned_data
