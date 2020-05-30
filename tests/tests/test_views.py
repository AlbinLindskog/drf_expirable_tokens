from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings

from drf_expirable_authtokens import ExpirableToken
from drf_expirable_authtokens import views


User = get_user_model()


urlpatterns = [
    url(r'^auth-token/$', views.obtain_expirable_token),
]


class ExpirableTokenTestCase(TestCase):

    def setUp(self):
        self.password, self.username = 'hunter1', 'dharoc'
        self.user = User(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    @override_settings(ROOT_URLCONF=__name__)
    @override_settings(EXPIRABLE_TOKEN_SALT='hejsvejs')
    def test_login_expirable_token(self):
        """Ensure that the login view returns a valid ExpirableToken."""
        client = Client()
        response = client.post(
            '/auth-token/',
            {'username': self.user.username, 'password': self.password}
        )
        self.assertEqual(response.status_code, 201)
        key = response.json()['token']
        self.assertEqual(ExpirableToken.from_key(key).user, self.user)
