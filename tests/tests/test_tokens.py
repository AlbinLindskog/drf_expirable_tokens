from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import now

from drf_expirable_authtokens import ExpirableToken


User = get_user_model()


class TestExpirableToken(ExpirableToken):
    salt = 'test'


class ExpirableTokenTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='dharoc')

    def test_invalidate_on_login(self):
        key = TestExpirableToken(user=self.user).key

        self.user.last_login = now()
        self.user.save()

        with self.assertRaises(TestExpirableToken.DoesNotExist):
            TestExpirableToken.from_key(key)

    def test_settings_priority(self):
        # First we check the default setting:
        self.assertEqual(TestExpirableToken.get_max_age(), 86400)

        # The we apply user provided django settings
        with self.settings(EXPIRABLE_TOKEN_MAX_AGE=12000, EXPIRABLE_TOKEN_SALT='hej'):
            self.assertEqual(TestExpirableToken.get_max_age(), 12000)

            # Which are still overridden by class attributes
            self.assertEqual(TestExpirableToken.get_salt(), 'test')

    def test_user_cache(self):
        """
        Regardless of how you init a ExpirableToken should the user attribute
        be cached and repeated access shouldn't require querying the db.
        """
        original_token = TestExpirableToken(user=self.user)
        token = TestExpirableToken.from_key(original_token.key)

        def test_init_cache():
            user = original_token.user

        def test_user_cache():
            user = token.user

        self.assertNumQueries(0, test_init_cache)
        self.assertNumQueries(0, test_user_cache)
