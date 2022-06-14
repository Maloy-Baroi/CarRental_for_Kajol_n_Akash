from django.forms import ModelForm
from App_authentication.models import CustomUser, Profile, ContactUsModel
from django.contrib.auth.forms import UserCreationForm


# forms
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2',)


class ContactUsForm(ModelForm):
    class Meta:
        model = ContactUsModel
        fields = "__all__"
