from django.utils import timezone
from rest_framework import serializers

from custom_auth.models import VerificationCode


class AuthRequestSerializer(serializers.Serializer):
    """Serialize request for auth."""

    email = serializers.EmailField()
    code = serializers.CharField(max_length=30)

    def validate_code(self, value):
        valid = VerificationCode.objects.filter(
            email=self.initial_data['email'],
            code=value,
            is_active=True,
            expire_at__gte=timezone.now()
        ).exists()
        if not valid:
            raise serializers.ValidationError("Код подтверждения неверный")

        return value


class VerificationCodeRequestSerializer(serializers.Serializer):
    """Serialize request for generate verification code."""

    email = serializers.EmailField()
