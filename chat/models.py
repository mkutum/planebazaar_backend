from django.db import models

# Create your models here.
from user.models import Users


class UserChat(models.Model):
    userchat_opt      =   models.ForeignKey(Users, on_delete=models.CASCADE, related_name='userchat_opt')
    userchat_vend     =   models.ForeignKey(Users, on_delete=models.CASCADE, related_name='userchat_vend')
    created_date      =   models.DateField(auto_now_add=True)

class Chat(models.Model):
    sender           = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sender')
    content          = models.TextField(max_length=500, null=True, blank=True)
    userchar_map_id  = models.ForeignKey(UserChat, on_delete=models.CASCADE)
    status_timestamp = models.DateTimeField(null=True, blank=True)
    created_date     = models.DateField(auto_now_add=True)
    active           = models.BooleanField(default=True)

