from django.db import models

# Create your models here.
from user.models import OrgUser, Users


class Notification(models.Model):
    notification      =     models.TextField(max_length=250)
    notification_type =     models.CharField(max_length=255, null=True, blank=True)
    action            =     models.URLField(max_length=255)
    created_time      =     models.DateField(auto_now_add=True)


class Receipient(models.Model):
    orguser_id         =    models.ForeignKey(OrgUser, on_delete=models.CASCADE, related_name='recipients')
    notification_id    =    models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='notifications')
    is_read            =    models.BooleanField(default=False)
    read_timestamp     =    models.DateTimeField(default=False)
    created_time       =    models.DateTimeField(auto_now_add=True)
    received_by_user_d =    models.ForeignKey(Users, on_delete=models.CASCADE, related_name='recipient')



