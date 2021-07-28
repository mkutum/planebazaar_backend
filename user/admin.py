from django.contrib import admin

# Register your models here.
from chat.models import *
from message.models import *
from rfq.models import *
from user.models import *
# User app Models
admin.site.register(Users)
admin.site.register(Organisation)
admin.site.register(OrgUser)
admin.site.register(Tags)
admin.site.register(Aircraft)
admin.site.register(OperatorVendor)

# Rfq app Models
admin.site.register(Rfq)
admin.site.register(Component)
admin.site.register(Parts)
admin.site.register(Consumable)
admin.site.register(Rfqs)
admin.site.register(Quotation)
admin.site.register(Pricing)
admin.site.register(ProcessStatus)
admin.site.register(Bookmarkquote)
admin.site.register(Flag)

# Chat app Models
admin.site.register(Chat)
admin.site.register(UserChat)

# Message app Models
admin.site.register(Notification)
admin.site.register(Receipient)

