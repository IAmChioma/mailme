from rest_framework import permissions, views
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import AuditTrailSerializer, AddAuditTrailSerializer, UpdateUserSerializer, UserProfileSerializer, MailingSerializer, AddMailingSerializer
from .models import Userprofile, Mailing, AuditTrail
from rest_framework.viewsets import ModelViewSet


class AuditTrailViewSet(ModelViewSet):
    queryset = AuditTrail.objects.all()
    serializer_class = AuditTrailSerializer
    # permission_classes = (permissions.IsAuthenticated.)


class UserProfileViewSet(ModelViewSet):
    queryset = Userprofile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class MailingViewSet(ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class AddMailingView(CreateAPIView):
    model = Mailing
    serializer_class = AddMailingSerializer


class AddAuditTrailView(CreateAPIView):
    model = AuditTrail
    serializer_class = AddAuditTrailSerializer


class UpdateUserView(UpdateAPIView):
    model = Userprofile
    serializer_class = UpdateUserSerializer
    queryset = Userprofile.objects.all()
    lookup_field = 'pk'
    permission_classes = (permissions.AllowAny,)