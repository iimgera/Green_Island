from rest_framework import serializers
from django.contrib.auth import authenticate

from apps.users.models import User


class BaseRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 
            'email', 
            'password', 
            'password_confirmation',
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation', None)


        if password != password_confirmation:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs


class OperatorRegistrationSerializer(BaseRegistrationSerializer):
    class Meta(BaseRegistrationSerializer.Meta):
        fields = BaseRegistrationSerializer.Meta.fields + (
            'full_name', 'user_type',
        )

    def create(self, validated_data):
        validated_data['user_type'] = 'OPERATOR'
        user = User.objects.create_user(**validated_data)
        return user


class BrigadeRegistrationSerializer(BaseRegistrationSerializer):
    application_count = serializers.SerializerMethodField()

    def get_application_count(self, obj):
        return obj.applications_as_brigade.count()
    
    class Meta(BaseRegistrationSerializer.Meta):
        fields = BaseRegistrationSerializer.Meta.fields + (
            'brigades_name', 
            'brigades_list', 
            'phone',
            'user_type', 
            'brigade_status',
            'application_count',
        )

    def create(self, validated_data):
        validated_data['user_type'] = 'BRIGADE'
        user = User.objects.create_user(**validated_data)
        return user


class BrigadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'brigades_name', 
            'brigades_list', 
            'phone',
            'user_type', 
            'brigade_status',
        )


class ClientRegistrationSerializer(BaseRegistrationSerializer):
    company_name = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()

    class Meta(BaseRegistrationSerializer.Meta):
        fields = BaseRegistrationSerializer.Meta.fields + (
            'email',
            'company_name',
            'address',
            'phone',
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует.")
        return value

    def create(self, validated_data):
            email = validated_data.get('email')
            password = validated_data.get('password')
            user = User.objects.create_user(
                email=email,
                password=password,
                user_type='CLIENT'
            )
            return user


class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'company_name',
            'address',
            'phone',
        )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.filter(email=email).first()
    
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email, password=password)

            if not user:
                message = 'Не удается войти в систему с предоставленными учетными данными.'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Должен содержать "адрес электронной почты" и "пароль".'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
        )
