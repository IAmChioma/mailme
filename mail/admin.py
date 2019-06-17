from django.contrib import admin
from .models import Mailing, Userprofile, AuditTrail
# Register your models here.
admin.site.register(Mailing)
admin.site.register(Userprofile)
admin.site.register(AuditTrail)