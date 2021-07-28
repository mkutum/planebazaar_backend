from django.db import models

# Create your models here.
from user.models import OrgUser, Users


class Rfq(models.Model):
    RFQ_TYPES = (
        ("PUBLIC", "Public"),
        ("PRIVATE", "Private"),
    )
    Priority_choice = (
        ("NORMAL", "Normal"),
        ("AOG", "AOG"),
        ("PRIORITY", "Priority")
    )
    orguser_id          =   models.ForeignKey(OrgUser, on_delete=models.CASCADE, related_name='rfq_user')
    rfq_type            =   models.CharField(max_length=250, choices=RFQ_TYPES, default="Public")
    short_description   =   models.CharField(max_length=300, null=True, blank=True)
    attachment          =   models.URLField(max_length=300, null=True, blank=True)
    created_date        =   models.DateTimeField(auto_now_add=True)
    draft_status        =   models.BooleanField(default=False)
    rfq_value           =   models.PositiveIntegerField()
    priority            =   models.CharField(max_length=250, choices=Priority_choice, default="Normal")
    is_dead             =   models.BooleanField(default=False)
    is_completed        =   models.BooleanField(default=False)

    def __str__(self):
        return str(self.rfq_type)


class Rfqs(models.Model): # Deadline of Rfq Details Model
    rfq_id              =   models.ForeignKey(Rfq, on_delete=models.CASCADE, related_name='rfq_deadline')
    deadline            =   models.DateTimeField()
    active              =   models.BooleanField(default=True)
    target_date         =   models.DateField()
    inactive_timestamp  =   models.DateTimeField(null=True, blank=True)
    created_date        =   models.DateField(auto_now_add=True)
    added_by_user       =   models.ForeignKey(Users, on_delete=models.CASCADE, related_name='deadline_edited_by')


class Component(models.Model):
    Component_Type = (
        ("PART", "PART"),
        ("CONSUMABLE", "Consumable"),
    )
    component_type   =   models.CharField(max_length=200, choices=Component_Type)
    rfq_id           =   models.ForeignKey(Rfq, on_delete=models.CASCADE, related_name='componet_for_rfq')
    created_time     =   models.DateField(auto_now_add=True)
    added_by_user    =   models.ForeignKey(Users, on_delete=models.CASCADE, related_name='components_added_by')

    """@property
    def consumables(self):
        return self.consumable_set.all()

    @property
    def parts (self):
        return self.parts_set.all()"""

class Consumable(models.Model):
    consumable_name     =    models.CharField(max_length=200)
    component_id        =    models.OneToOneField(Component, on_delete=models.CASCADE, related_name='consumables')
    description         =    models.TextField(max_length=300)
    quantity            =    models.PositiveIntegerField()
    quantity_type       =    models.CharField(max_length=100)
    consumable_number   =    models.IntegerField()
    certifications      =    models.TextField(max_length=500,null=True, blank=True)
    created_time        =    models.DateField(auto_now_add=True)
    added_by_user       =    models.ForeignKey(Users, on_delete=models.CASCADE)


class Parts(models.Model):
    part_name       =   models.CharField(max_length=300, blank=True, null=True)
    part_number     =   models.IntegerField()
    description     =   models.TextField(max_length=300)
    component_id    =   models.OneToOneField(Component, on_delete=models.CASCADE, related_name='parts')
    manufacturer    =   models.CharField(max_length=200)
    quantity        =   models.IntegerField()
    certifications  =   models.TextField(max_length=500, blank=True, null=True)
    created_time    =   models.DateField(auto_now_add=True)
    added_by_user   =   models.ForeignKey(Users, on_delete=models.CASCADE)


class Quotation(models.Model):
    orguser_id          =   models.ForeignKey(OrgUser, on_delete=models.CASCADE, related_name='users')
    rfq_id              =   models.ForeignKey(Rfq, on_delete=models.CASCADE, related_name='rfq')
    quotation           =   models.URLField(null=True, blank=True)
    description         =   models.TextField(max_length=255, null=True, blank=True)
    is_completed        =   models.BooleanField(default=False)
    is_cancelled        =   models.BooleanField(default=False)
    tax                 =   models.DecimalField(max_digits=10,decimal_places=3, null=True, blank=True)
    shipping_cost       =   models.IntegerField(null=True, blank=True)
    quotation_closed    =   models.BooleanField(default=False)
    delivery_date       =   models.DateField(default=False)
    created_date        =   models.DateField(auto_now_add=True)
    #edited_by_user      =   models.ForeignKey(Users, on_delete=models.CASCADE)


class Pricing(models.Model):
    quotation_id    =   models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='quotation_pricing')
    component_id    =   models.ForeignKey(Component, on_delete=models.CASCADE, related_name='component_pricing')
    unit_type       =   models.CharField(max_length=255)
    unit_price      =   models.PositiveIntegerField()
    manufacturer    =   models.CharField(max_length=255)
    serial_number   =   models.IntegerField()
    active          =   models.BooleanField(default=True)
    created_date    =   models.DateField(auto_now_add=True)
    #edited_by_user  =   models.ForeignKey(Users, on_delete=models.CASCADE)


class PricingChange(models.Model):
    pricing_id      =     models.ForeignKey(Pricing, on_delete=models.CASCADE, related_name='pricing_change')
    unit_price      =   models.PositiveIntegerField()
    active          =   models.BooleanField(default=True)
    created_date    =   models.DateField(auto_now_add=True)
    edited_by_user  =   models.ForeignKey(Users, on_delete=models.CASCADE)




class Attachment(models.Model):
    # ProcessStatus Model which will contains all details about rfq after quotation is awarded to still final invoice
    quotation_id        =   models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='rfqquotes')
    active              =   models.BooleanField(default=True)
    performa            =   models.URLField(null=True, blank=True)
    po                  =   models.URLField(null=True, blank=True)
    final_invoice       =   models.URLField(null=True, blank=True)
    inactive_timestamp  =   models.DateTimeField(default=False)
    created_date        =   models.DateField(auto_now_add=True)


class ProcessStatus(models.Model):
    rfq_attachment_id   =   models.ForeignKey(Attachment, on_delete=models.CASCADE)
    status              =   models.CharField(max_length=250)
    active              =   models.BooleanField(default=True)
    created_date        =   models.DateField(auto_now_add=True)
    edited_by_user      =   models.ForeignKey(Users, on_delete=models.CASCADE)


class Bookmarkquote(models.Model):
    # bookmarkquote is model has details about quotation bookmarked by operator
    quotation_id       =    models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='bookmarkedquote')
    active             =    models.BooleanField(default=True)
    created_date       =    models.DateField(auto_now_add=True)
    bookmarked_by_user =    models.ForeignKey(Users, on_delete=models.CASCADE)


class Flag(models.Model):
    quotation_id        =    models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='flagedrfq')
    comment             =    models.TextField(max_length=500)
    status              =    models.CharField(max_length=200)
    active              =    models.BooleanField(default=True)
    flaged_by_user      =    models.ForeignKey(Users, on_delete=models.CASCADE)

class FlagChange(models.Model):
    flag_id             =    models.ForeignKey(Flag, on_delete=models.CASCADE, related_name='flag_changed')
    active              =    models.BooleanField(default=True)
    created_date        =    models.DateField(auto_now_add=True)
    flaged_by_user      =    models.ForeignKey(Users, on_delete=models.CASCADE)

