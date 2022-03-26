import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_auth.models import VerificationCode
from custom_auth.serializers import AuthRequestSerializer, VerificationCodeRequestSerializer


# todo add docs
class AuthView(APIView):
    """
    Get auth token for user.

    Register user if not registered and return token.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Return auth token already registered or new user."""
        serializer = AuthRequestSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = self._get_or_create_user(serializer.validated_data['email'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

    def get(self, request, *args, **kwargs):
        """Send verification code to email."""
        serializer = VerificationCodeRequestSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        if not self._check_time(email):
            return Response(
                {'error': 'Между отправками кода подтверждения должна пройти 1 минута.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        validation_code_object = self._create_verification_code(email)
        # todo send email
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def _get_or_create_user(email: str) -> User:
        user, _created = User.objects.get_or_create(
            email=email,
        )
        return user

    @staticmethod
    def _check_time(email: str) -> bool:
        """Check that more than a minute has passed since the last creation verification code."""
        return not VerificationCode.objects.filter(
            email=email,
            created__gte=timezone.now() - timedelta(minutes=1)
        ).exists()

    @staticmethod
    def _create_verification_code(email: str) -> VerificationCode:
        random.seed()
        code = str(random.randint(10000, 99999))
        expire_at = timezone.now() + timedelta(minutes=15)

        return VerificationCode.objects.create(email=email, code=code, expire_at=expire_at)



