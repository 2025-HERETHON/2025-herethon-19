from django import forms

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("new_password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return cleaned_data