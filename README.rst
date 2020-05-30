DRF expirable auth tokens
-------------------------------------
Drop in replacement for Django REST framework's TokenAuthentication with
stateless expirable tokens, far more appropriate for web application-server
setups.

Setup
^^^^^
To use the ExpirableTokenAuthentication scheme you'll need to configure the
authentication classes to include ExpirableTokenAuthentication.::

     REST_FRAMEWORK = {
        ...
        'DEFAULT_AUTHENTICATION_CLASSES': (
            drf_expirable_tokens.ExpirableTokenAuthentication,
            ...
        ),
     }

You'll also need to create tokens for your users::

    from drf_expirable_tokens import ExpirableToken

    token = ExpirableToken(user=...)
    print(token.key)

When using ExpirableTokenAuthentication, you may want to provide a mechanism
for clients to obtain a token themselves given the username and password.
drf_expirable_authtokens provides a built-in view to provide this behavior. To
use it, add the obtain_expirable_token view to your URLconf::

    from drf_expirable_authtokens import views
    urlpatterns += [
        url(r'^login/', views.obtain_expirable_token)
    ]

The obtain_auth_token view will return a JSON response containing a token the
client can use to authenticate themselves with when valid username and password
are POST:ed to the view.::

    {'token': 'eyJuYXRfa2V5IjoiZGhhcm9jIiwibGFzdF9sb2dpbiI6bnVsbH0:1jexQY:k9lgfAGU0mb1pr1FKWCGtGeLmyU'}

For clients to authenticate, the token key should be included in the
Authorization HTTP header. The key should be prefixed by the string literal
"Token", with whitespace separating the two strings. For example::

    Authorization: Token eyJuYXRfa2V5IjoiZGhhcm9jIiwibGFzdF9sb2dpbiI6bnVsbH0:1jexQY:k9lgfAGU0mb1pr1FKWCGtGeLmyU


Settings
^^^^^^^^
These are the configurable defaults settings.

EXPIRABLE_TOKEN_MAX_AGE (int): The lifetime of the token in seconds before its
    key becomes invalid. Defaults to 86400, i.e. one day.

EXPIRABLE_TOKEN_SALT (str): Salt used in the signature. Defaults to
    'drf_expirable_authtokens.salt'. Leaving this as the default or using the
    same salt for different projects is a security risk.

EXPIRABLE_TOKEN_RAISE_INVALID (bool): Whether to raise AuthenticationFailed if
    a user provides an invalid token. Defaults to True. Setting this to False
    allows you to use both ExpirableTokenAuthentication and
    TokenAuthentication with the same keyword in the same project. If this is
    True will ExpirableTokenAuthentication raise  AuthenticationFailed and
    short circuit the authentication when it encounters a regular
    authentication token, since those are not valid ExpirableTokens.

Development
^^^^^^^^^^^
To run the tests; clone the repository, setup the virtual environment, and run
the tests.::

    # Setup the virtual environment
    $ virtualenv test_env
    $ source test_env/bin/activate
    $ pip3 install -r test_requirements.txt

    # Run the tests
    $ cd tests
    $ python3 manage.py test
