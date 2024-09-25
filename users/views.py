from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import *


class RegisterUserApiView(GenericAPIView):
    """
    registers a user to the platform
    """
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.data['email'])
            data = {
                "message": "User created successfully",
                "otp": user.otp_code
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmOtpAPiView(GenericAPIView):
    """
    confirms a users OTP
    """
    serializer_class = OtpConfirmationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = {
                "message": "OTP code confirmed successfully",
                "exists": True
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendOtpApiView(GenericAPIView):
    """
    resends a user confirmation OTP
    """
    serializer_class = ResendOtpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = request.data['email']
            user = User.objects.get(email=email)
            otp = create_user_otp()
            user.otp_code = otp
            user.save()
            user.send_otp()
            data = {
                "message": "OTP resent to provided email"
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PhonenumberOTPRegisterApiView(GenericAPIView):
    """
    registes user then sends an OTP code to a users phonenumber
    """
    serializer_class = PhonenumberRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = create_user_otp()
            user = User.objects.create(
                phone_number=phone_number,
                phone_otp_registration=True,
                email=f"{phone_number}@forge.com"
            )
            user.otp_code = otp
            user.save()
            user.send_phonenumber_opt()
            data = {
                "message": "OTP sent to provided Phonenumber",
                "otp": otp
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PhonenumberSendOTPApiView(GenericAPIView):
    """
    sends otp code to a users phonenumber
    """
    serializer_class = PhonenumberSendOtpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['phone_number']
            otp = create_user_otp()
            user.otp_code = otp
            user.save()
            usr = User.objects.get(phone_number=user.phone_number)
            sms = usr.send_phonenumber_opt()
            print(sms)
            if not sms:
                data = {
                    "message": "User created, but error sending OTP, resend OTP to number.",
                    "errored_otp": otp,
                }
            else:
                data = {
                    "message": "OTP sent to provided Phonenumber",
                    "otp": otp
                }                
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetUserPasswordApiView(GenericAPIView):
    """
    sets the user password and returns JWT token
    """
    serializer_class = SetUserPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data_dict = serializer.data
            otp = data_dict['otp_code']
            password = data_dict['password']
            user = User.objects.get(otp_code=otp)
            user.update_user_password(password)
            refresh_token = RefreshToken.for_user(user)
            user_serializer = UsersSerializer(user)
            data = {
                "message": "Password set successfully",
                "user": user_serializer.data,
                "refresh": f"{refresh_token}",
                "access": f"{refresh_token.access_token}"
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserApiView(GenericAPIView):
    """
    gets, updates and deletes user
    """
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        serializer = UsersSerializer(user)
        serializer_data = serializer.data
        user.delete()
        data = {
            "message": "Deleted User successfully",
            "user": serializer_data
        }
        return Response(data)


class ChangeUserPasswordApiView(GenericAPIView):
    """
    changes a user password from current one
    """  
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            usr = authenticate(
                username=user.email,
                password=request.data['old_password']
            )
            if usr is not None:
                user.set_password(request.data['password'])
                user.save()
                data = {
                    'message': 'User password changed successfully'
                }
                return Response(data)
            else:
                data = {
                    'message': 'Incorrect old password set'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileApiView(GenericAPIView):
    """
    gets a users profile
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.filter(
            user=request.user
        ).first()
        serializer = self.serializer_class(profile)
        return Response(serializer.data)
    

class ProfileModifyApiView(GenericAPIView):
    """
    updates a profile
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        profile = Profile.objects.filter(id=id).first()
        if profile is None:
            data = {
                "message": f"No Profile Service object found with id {id}"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailCheckApiView(GenericAPIView):
    """
    checks if an email exist
    """
    serializer_class = EmailCheckSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            exists = User.objects.filter(email=request.data['email']).exists()
            data = {
                "message": "Email Confirmed Successfully",
                "exists": exists
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)