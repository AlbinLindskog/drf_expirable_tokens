from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, override_settings

from rest_framework.exceptions import AuthenticationFailed

from drf_expirable_authtokens import ExpirableToken, ExpirableTokenAuthentication


User = get_user_model()


class RaiseExpirableTokenAuthentication(ExpirableTokenAuthentication):
    raise_invalid = True


@override_settings(EXPIRABLE_TOKEN_SALT='override')
class ExpirableTokenAuthenticationTestCase(TestCase):
    authenticator = ExpirableTokenAuthentication()

    def setUp(self):
        self.user = User.objects.create(username='dharoc')

    def test_valid_token(self):
        token = ExpirableToken(self.user)
        headers = {'HTTP_AUTHORIZATION': 'Token ' + token.key}
        request = RequestFactory().get('/', **headers)

        user, token = self.authenticator.authenticate(request)

        self.assertEqual(user, self.user)

    def test_invalid_token(self):
        headers = {'HTTP_AUTHORIZATION': 'Token ' + 'invalid'}
        request = RequestFactory().get('/', **headers)

        with self.assertRaises(AuthenticationFailed):
            user, token = self.authenticator.authenticate(request)

    def test_settings_priority(self):
        # First we check the default setting:
        self.assertEqual(ExpirableTokenAuthentication.get_raise_invalid(), True)

        # The we apply user provided django settings
        with self.settings(EXPIRABLE_TOKEN_RAISE_INVALID=False):
            self.assertEqual(ExpirableTokenAuthentication.get_raise_invalid(), False)

            # Which are still overriden by class attributes
            self.assertEqual(RaiseExpirableTokenAuthentication.get_raise_invalid(), True)

    @override_settings(EXPIRABLE_TOKEN_RAISE_INVALID=False)
    def test_raise_invalid_is_false(self):
        headers = {'HTTP_AUTHORIZATION': 'Token ' + 'invalid'}
        request = RequestFactory().get('/', **headers)

        result = self.authenticator.authenticate(request)
        self.assertIsNone(result)

    def test_fail_if_inactive_user(self):
        token = ExpirableToken(self.user)
        headers = {'HTTP_AUTHORIZATION': 'Token ' + token.key}
        request = RequestFactory().get('/', **headers)

        self.user.is_active = False
        self.user.save()

        with self.assertRaises(AuthenticationFailed):
            user, token = self.authenticator.authenticate(request)
