from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import DeactivateUserSerializer, SupervisorSerializer, UserSerializer, \
    ChangePasswordSerializer, ResetPasswordSerializer, MgtSerializer, SecureIDSerializer, \
    TellerSerializer, ChangePassSerializer, LoginSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from django.contrib.auth import get_user_model
from django.db import connection
import collections
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode, int_to_base36
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import AllowAny


UserModel = get_user_model()

class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def group_names(self, request, pk=None):
        """
        Returns a list of all the group names that the given
        user belongs to.
        """
        user = self.get_object()
        groups = user.groups.all()
        return Response([group.name for group in groups])


class LoginView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"))

        if user is None or not user.is_active:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username or password incorrect'
            }, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response(LoginSerializer(user).data)


class LogoutView(views.APIView):

    def get(self, request):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CreateUserView(CreateAPIView):

    model = get_user_model()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class CreateSecureIDView(CreateAPIView):

    model = get_user_model()
    serializer_class = SecureIDSerializer
    permission_classes = (AllowAny,)


class CreateSupervisorView(CreateAPIView):

    model = get_user_model()
    serializer_class = SupervisorSerializer
    permission_classes = (AllowAny,)


class CreateMgtView(CreateAPIView):
    model = get_user_model()
    serializer_class = MgtSerializer
    permission_classes = (AllowAny,)


class CreateTellerView(CreateAPIView):

    model = get_user_model()
    serializer_class = TellerSerializer
    permission_classes = (AllowAny,)


class DeactivateUserView(UpdateAPIView):
    model = UserModel
    serializer_class = DeactivateUserSerializer
    queryset = UserModel.objects.all()
    lookup_field = 'pk'


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
   # serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def get_object(self, queryset=None):
        return self.request

    def post(self,request, domain_override=None,use_https=False, token_generator=default_token_generator, from_email=None, html_email_template_name=None, *args, **kwargs):
        self.object = self.get_object()
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email_address = serializer.data.get("email_address")
            active_users = UserModel._default_manager.filter(
                email__iexact=email_address, is_active=True)
            for user in active_users:
                if not user.has_usable_password():
                    continue
                if not domain_override:
                    current_site = '127.0.0.0:8000'
                    site_name = 'Fuel Management System'
                    domain = current_site
                else:
                    site_name = domain = domain_override
                subject = 'Reset Your Password'
                message = render_to_string('pasword_reset.html', {
                  #  'email': user.email,
                    'domain': domain,
                    'site_name': site_name,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'user': user,
                    'token': token_generator.make_token(user),
                    'protocol': 'https' if use_https else 'http',
                })
                user.email_user(subject, message)
               # from_email = settings.EMAIL_HOST_USER
               # to_list = [user.email, settings.EMAIL_HOST_USER]
                to_list = [email_address]
             #   send_mail(subject, message, from_email, to_list, fail_silently=True)
                print("Kindly check your mail to reset your password")

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ResetAfterMail(APIView):
    """
    An endpoint for changing password.
    """
   # authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny, )

    def get_object(self, queryset=None):

        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePassSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            user_id = serializer.data.get("user_id")
            user= User.objects.get(id=user_id)
            # username_1 =user.username
            # password_1 = user.password
            # user = authenticate(username=username_1, password=password_1)
            # login(request, user)
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            if old_password != new_password:
                return Response({"Password mismatch": ["Password doesnt match."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            logout(request)
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class check_user_id(object):
    def check_uid(user_id):
        try:
            uid = force_text(urlsafe_base64_decode(user_id))
            user = User.objects.get(pk=uid)

            return user
        except User.DoesNotExist:
            return None


class UserDetails(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = check_user_id.check_uid(
            user_id=request.data.get("user_id"), )

        if user is None:
            return Response({
                'status': 'No such category',
                'message': 'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)

        else:

            login(request, user)
            return Response(UserSerializer(user).data)
