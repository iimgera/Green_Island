from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.serializers import (
    OperatorRegistrationSerializer, BrigadeRegistrationSerializer,
    ClientRegistrationSerializer, ClientProfileSerializer,
    UserLoginSerializer, ResetPasswordSerializer
)
from apps.users.permissions import OperatorPermission


class OperatorListView(generics.ListAPIView):
    queryset = User.objects.filter(user_type='OPERATOR')
    serializer_class = OperatorRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class OperatorRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = OperatorRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated, OperatorPermission]
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(user_type='OPERATOR')
        refresh = RefreshToken.for_user(user)

        return Response({
            'user_id': user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': user.user_type,
        }, status=status.HTTP_201_CREATED)


class OperatorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(user_type='OPERATOR')
    serializer_class = OperatorRegistrationSerializer
    permission_classes = [OperatorPermission]


class BrigadeRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = BrigadeRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated, OperatorPermission, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(user_type='BRIGADE')
        refresh = RefreshToken.for_user(user)

        return Response({
            'user_id': user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': user.user_type,
        }, status=status.HTTP_201_CREATED)


class BrigadeListView(generics.ListAPIView):
    queryset = User.objects.filter(user_type='BRIGADE')
    serializer_class = BrigadeRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class BrigadeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(user_type='BRIGADE')
    serializer_class = BrigadeRegistrationSerializer
    permission_classes = [OperatorPermission]


class ClientRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ClientRegistrationSerializer
    permission_classes = [permissions.AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(user_type='CLIENT')
        refresh = RefreshToken.for_user(user)

        return Response({
            'user_id': user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': user.user_type,
            'email': user.email,
            'address': user.address,
            'phone': user.phone,
        }, status=status.HTTP_201_CREATED)


class ClientProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type='CLIENT')
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    @action(detail=False, methods=['get'])
    def profile(self, request, user_id=None):
        queryset = User.objects.filter(id=user_id or request.user.id)
        user = get_object_or_404(queryset)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def edit(self, request, user_id=None):
        queryset = User.objects.filter(id=user_id or request.user.id)
        user = get_object_or_404(queryset)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if not user.is_active:
            return Response(
                {'error': 'Учетная запись пользователя отключена.'},
                status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'user_id': user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': user.user_type,
        }, status=status.HTTP_200_OK)


class ResetPasswordAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {'error': 'Пользователь с данным электронным адресом не найден'}, status=400
                )
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            send_mail(
                'Password Reset Request',
                f'Ваш новый пароль  {password}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response({'success': 'Отправлено электронное письмо для сброса пароля'})
        return Response({'error': 'Поле электронной почты обязательно для заполнения'}, status=400)
