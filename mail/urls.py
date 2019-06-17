from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from .api import MailingViewSet, AuditTrailViewSet, UserProfileViewSet, AddAuditTrailView, AddMailingView, UpdateUserView
router = DefaultRouter()

router.register('mailing', MailingViewSet)
router.register('audit', AuditTrailViewSet)
router.register('profile', UserProfileViewSet)

urlpatterns = router.urls

urlpatterns += [
    url('addmail/$', AddMailingView.as_view()),
    url('addtransaction/$', AddAuditTrailView.as_view()),
    url('user/update/(?P<pk>\d+)/$', UpdateUserView.as_view())

]
