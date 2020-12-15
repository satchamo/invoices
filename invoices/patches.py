"""
Monkey patch the password reset form so they give more helpful error messages
"""
from django import forms as foo
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.utils.timezone import now
from datetime import timedelta
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

try:
    from django.utils.text import mark_safe
except ImportError:
    from django.utils.html import mark_safe


def _clean_email(self, fn=getattr(PasswordResetForm, "clean_email", lambda self: self.cleaned_data['email'])):
    from django.contrib.auth import get_user_model
    email = self.cleaned_data['email']
    UserModel = get_user_model()
    if UserModel.objects.filter(email=email).count() == 0:
        raise foo.ValidationError("A user with that email address does not exist!", code="unknown-email")

    if UserModel.objects.filter(email=email, is_active=True).count() == 0:
        raise foo.ValidationError("It looks like you tried to sign up for an account, but never paid for it. You need to sign up again.", code="inactive-account")

    return fn(self)

PasswordResetForm.clean_email = _clean_email


def _clean_username(self, fn=getattr(AuthenticationForm, "clean_username", lambda self: self.cleaned_data['username'])):
    from django.contrib.auth import get_user_model
    username = self.cleaned_data.get('username')
    UserModel = get_user_model()
    if username and not UserModel.objects.filter(**{UserModel.USERNAME_FIELD: username}).exists():
        raise foo.ValidationError(mark_safe("That username is incorrect. If you forgot it, you can <a href='%s'>reset your password</a> (the password reset email contains your username)." % reverse("password_reset")), code="username")

    return fn(self)

AuthenticationForm.error_messages['invalid_login'] = "That password is incorrect"
AuthenticationForm.error_messages['inactive'] = "You tried to sign up for an account, but you never paid, so your account is not active. You need to sign up again."

AuthenticationForm.clean_username = _clean_username


def _init_password_change_form(self, *args, fn=PasswordChangeForm.__init__, **kwargs, ):
    """
    Give people some time to change their password without entering the old
    password. Entering the old password is kinda pointless anyway, since they
    can just update the email address and send a password reset email. It
    doesn't give any extra security.
    """
    fn(self, *args, **kwargs)
    from django.utils.timezone import now

    joined = getattr(self.user, "date_joined", None)
    if not joined:
        joined = getattr(self.user, "DateJoined")

    last_login = getattr(self.user, "last_login", None)
    if not last_login:
        last_login = getattr(self.user, "LastLogin")

    grace_period = timedelta(hours=36)
    if abs(now() - joined) < grace_period:
        self.fields.pop("old_password")

PasswordChangeForm.__init__ = _init_password_change_form
