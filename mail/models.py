import sys
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from io import BytesIO


# Create your models here.

class Userprofile(models.Model):
    id = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    image = models.ImageField(upload_to='profile', max_length=50, default='default.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    email = models.EmailField()
    sex = models.CharField(max_length=7, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    STATUSES = (
        ('Sta', 'Staff'),
        ('Not', 'NotStaff'),

    )
    is_staff = models.CharField(max_length=3, choices=STATUSES, default='Sta', help_text='Staff Status')

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        im = Image.open(self.image)

        output = BytesIO()

        # Resize/modify the image
        im = im.resize((200, 200))

        # after modifications, save it to the output
        im.save(output, format='PNG', quality=100, optimize=True, dpi=(300, 300))
        output.seek(0)

        # change the image field value to be the newley modifed image value
        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0],
                                          'image/jpeg',
                                          sys.getsizeof(output), None)

        super(Userprofile, self).save()

    def __str__(self):
        return "User {}".format(self.id)


class Mailing(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.TimeField(auto_now=True, null=True, blank=True)
    created_date = models.DateField(auto_now=True, null=True, blank=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    receiver = models.CharField(max_length=100)
    attachment= models.ImageField(upload_to='attachement', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="teller")
    STATUSES = (
        ('Rec', 'Received'),
        ('Del', 'Delivered'),
        ('Red', 'Read'),

    )
    status = models.CharField(max_length=3, choices=STATUSES, null=True, help_text='Transaction Status', blank=True)

    def __str__(self):
        return "{}".format(self.id)

class AuditTrail(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.TimeField(auto_now=True, null=True, blank=True)
    created_date = models.DateField(auto_now=True, null=True, blank=True)
    user_acting = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="device_station")
    action = models.TextField()

    def __str__(self):
        return "{}".format(self.action)