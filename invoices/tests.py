from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.test import TestCase
from model_mommy.mommy import make


class PatchesTestCase(TestCase):
    def test_auth_form_warns_if_username_does_not_exist(self):
        # username doesn't exist yet
        form = AuthenticationForm(None, {
            "username": "foo"
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("username", code="username"))

        make(get_user_model(), username="foo")
        # username does exist now
        form = AuthenticationForm(None, {
            "username": "foo"
        })
        self.assertFalse(form.is_valid())
        self.assertFalse(form.has_error("username", code="username"))

    def test_password_reset_form_gives_warning_if_email_address_does_not_exist(self):
        # email doesn't exist yet
        form = PasswordResetForm({
            "email": "foo@example.com"
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("email", code="unknown-email"))

        make(get_user_model(), email="foo@example.com", is_active=False)
        # email does exist now, but is inactive
        form = PasswordResetForm({
            "email": "foo@example.com"
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("email", code="inactive-account"))

        make(get_user_model(), email="foo@example.com", is_active=True)
        # email does exist now, but is inactive
        form = PasswordResetForm({
            "email": "foo@example.com"
        })
        self.assertTrue(form.is_valid())
