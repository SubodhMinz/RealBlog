from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Comment

# contact form
class  ContactForm(forms.Form):
    name = forms.CharField(label='Full Name', required=True)
    email = forms.EmailField()
    phone = forms.IntegerField(widget=forms.NumberInput)
    desc = forms.CharField(widget=forms.Textarea, label='Message', required=True)


# sign up form
class SignUpForm(UserCreationForm):
    username = UsernameField(
        error_messages = {'required':"Enter Username."},
    )
    email = forms.EmailField(
        label="Email",
        error_messages = {'required':"Enter Email."},
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        error_messages = {'required':"Enter Password."},
    )
    password2 = forms.CharField(
        label=_("Password confirm (again)"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        error_messages = {'required':"Enter Password Again."},
    )

    class Meta:
        model = User
        fields = ("username","email")



# Profile Update Form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']


# lgoin form
class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={
            "autofocus": True,
            "autocomplete": "current-username"
        }),
        error_messages = {'required':"Enter Your Username."},
        )
    email = forms.EmailField(
        label="Email",
        error_messages = {'required':"Enter Your Email."}
        )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        error_messages = {'required':"Enter Your Password."},
    )

    class Meta:
        model = User
        fields = ("email")

    def clean_email(self):
        valemail = self.cleaned_data['email']
        valname = self.cleaned_data['username']
        if len(valemail) <= 11:
            raise forms.ValidationError('Email Length Should Be Greater than 11 Charector.')
        if User.objects.filter(email=valemail).exists() and (User.objects.get(username=valname).email)==valemail:
            #  if User.objects.get(username=uname)
            # a = User.objects.filter(email=valemail).values('email')
            # print(a == valemail)
            # print(a.email)
            pass
        else:
            raise forms.ValidationError('Wrong Email ID.')
        return valemail


# Password Change Form
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        error_messages = {'required':"Enter Old Password."},
        label=_("Old Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete':'current-password',
                'autofocus':True
            }
        )
    )
    new_password1 = forms.CharField(
        error_messages = {'required':"Enter New Password."},
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete':'new-password'}),
            help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        error_messages = {'required':"Confirm New Password."},
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete':'new-password'}
        )
    )

# password reset form
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete':'email'}
        )
    )

# password set form
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(
            attrs={'autocomplete':'new-password'}
        ),
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete':'new-pssword'})
    )

# blog Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        labels = {'message':''}
