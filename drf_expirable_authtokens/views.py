from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .tokens import ExpirableToken


class ObtainExpirableToken(ObtainAuthToken):
    """
    View used by clients to obtain an ExpirableToken given a username and
    password.

    Returns a JSON response containing the token when valid username and
    password fields are POSTed to the view. The response has the format:

        {'token': 'eyJuYXRfa2V5IjoiZGhhcm9jIiwibGFzdF9sb2dpbiI6bnVsbH0:1jexQY:k9lgfAGU0mb1pr1FKWCGtGeLmyU'}
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = ExpirableToken(user)
        return Response({'token': token.key}, status=HTTP_201_CREATED)


obtain_expirable_token = ObtainExpirableToken.as_view()