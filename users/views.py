from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminOrIsMe, IsAnonymousOrAdmin
from .serializers import UserSerializer, AuthLoginSerializer, ResetPasswordSerializer, ChangePasswordSerializer, RequestCodeSerializer
from .models import User


class AuthViewSet(viewsets.ViewSet):
    serializer_class = AuthLoginSerializer

    @action(detail=False, url_path="request-code", methods=["post"])
    def request_code(self, request):
        serializer = RequestCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"status": "success"})

    @action(detail=False, url_path='login', methods=['post'])
    def login(self, request):
        data = AuthLoginSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        email = data.validated_data.get("email")
        password = data.validated_data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
            })

        raise AuthenticationFailed()

    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request):
        data = ResetPasswordSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        res = data.send_email()

        return Response(data=res)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrIsMe]

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAnonymousOrAdmin()]
        else:
            return [permission() for permission in self.permission_classes]

    @action(detail=False, url_path='me', methods=['get'], permission_classes=[IsAuthenticated])
    def get_my_user(self, request):
        return Response(data=self.serializer_class(request.user).data)

    @get_my_user.mapping.patch
    def update_my_user(self, request):
        serializer = self.serializer_class

        data = serializer(request.user, data=request.data, partial=True)
        data.is_valid(raise_exception=True)

        data.save()

        return Response(data=serializer(request.user).data)

    @action(detail=False, methods=['post'], url_path='me/change-password', permission_classes=[IsAuthenticated])
    def change_password(self, request):
        data = ChangePasswordSerializer(data=request.data, user=request.user)
        data.is_valid(raise_exception=True)

        return Response(data=data.update_password())

    @action(detail=True, methods=['post'], url_path='change-password/(?P<token_pk>[^/.]+)')
    def change_password_with_token(self, request, token_pk, pk):
        data = ChangePasswordSerializer(data=request.data, user_pk=pk, token_pk=token_pk)
        data.is_valid(raise_exception=True)

        return Response(data=data.update_password())
