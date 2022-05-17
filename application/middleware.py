from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import AccessToken


class SocialAuth(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super(SocialAuth, self).__init__(*args, **kwargs)

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        if user:
            return user, validated_token
        else:
            return None

    def get_user(self, validated_token: AccessToken):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token['vk_id']
        except KeyError:
            return None
        try:
            user = self.user_model.objects.get(**{'vk_id': user_id})

        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(_('User is inactive'), code='user_inactive')

        return user

