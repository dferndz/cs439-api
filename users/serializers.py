from rest_framework import serializers
from rest_framework.exceptions import NotFound, NotAuthenticated, APIException, AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.validators import UniqueValidator

from .models import User, PasswordToken
from .exceptions import PasswordDoNotMatchException, InvalidEidException


class RequestCodeSerializer(serializers.Serializer):
    csid = serializers.SlugRelatedField(slug_field="csid", queryset=User.objects.all())
    eid = serializers.CharField()

    def validate(self, attrs):
        user = attrs.get("csid")
        eid = attrs.get("eid")

        if user.eid is not None and user.eid != eid:
            raise InvalidEidException()

        return attrs

    def save(self, **kwargs):
        user = self.validated_data.get("csid")
        user.generate_code()
        if user.eid is None:
            user.eid = self.validated_data.get("eid")
            user.save()


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        email = validated_data.get('email', None)
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)

        if email is not None:
            instance.email = email

        if first_name is not None:
            instance.first_name = first_name

        if last_name is not None:
            instance.last_name = last_name

        instance.save()

        return instance

    def create(self, validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        instance = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        return instance


class AuthLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user', None)
        self.token_pk = kwargs.get('token_pk', None)
        self.user_pk = kwargs.get('user_pk', None)

        if self.user is not None:
            kwargs.pop('user')

        if self.token_pk is not None:
            kwargs.pop('token_pk')

        if self.user_pk is not None:
            kwargs.pop('user_pk')

        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if not self.user or not self.user.is_authenticated:
            if self.token_pk is None or self.user_pk is None:
                raise NotAuthenticated()
            try:
                self.user = User.objects.get(pk=self.user_pk)
            except ObjectDoesNotExist:
                raise AuthenticationFailed()

            if not PasswordToken.objects.use_token(self.user, self.token_pk):
                raise AuthenticationFailed()

        if password != password2:
            raise PasswordDoNotMatchException()

        return attrs

    def update_password(self):
        password = self.validated_data.get('password')

        if self.is_valid():
            self.user.set_password(password)
            self.user.save()

            return {
                'detail': 'password_changed',
                'user': self.user.pk
            }
        raise APIException(code=500)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        email = attrs.get('email')

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise NotFound()

        self.user = user

        return attrs

    def send_email(self):
        if self.user is not None and self.user.is_authenticated:

            self.user.reset_password()

            return {
                "detail": "email_sent"
            }
        raise NotFound()
