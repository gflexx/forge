from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import *
from .utils import create_user_otp


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def create(self, validated_data):
        otp = create_user_otp()
        user = User.objects.create(
            email=validated_data['email'],
            otp_code=otp
        )
        user.save()
        return user
    

class OtpConfirmationSerializer(serializers.Serializer):
    otp_code = serializers.IntegerField(required=True)

    def validate_otp_code(self, value):
        exists = User.objects.filter(otp_code=value).exists()
        if not exists:
            raise serializers.ValidationError("OTP code entered does not exist.")
        return value
    
    
class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        exists = User.objects.filter(email=value).exists()
        if not exists:
            raise serializers.ValidationError("Email entered does not exist.")
        return value
    
    
class SetUserPasswordSerializer(OtpConfirmationSerializer):
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs


class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        self.fields["user"] = UsersSerializer(read_only=True)
        return super(ProfileSerializer, self).to_representation(instance)
    

class PhonenumberRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        validators=[RegexValidator(r"^\+[1-9]\d{10,14}$")]
    )

    def validate_phone_number(self, value):
        user = User.objects.filter(phone_number=value)
        if user.exists():
            raise serializers.ValidationError("User with Phonenumber entered already exist.")
        return value
    

class PhonenumberSendOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        validators=[RegexValidator(r"^\+[1-9]\d{10,14}$")]
    )

    def validate_phone_number(self, value):
        user = User.objects.filter(phone_number=value).first()
        if not user:
            raise serializers.ValidationError("User with Phonenumber entered does not exist.")
        return user