from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email,password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email),)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email=self.normalize_email(email), password=password,)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    user_name           =    models.CharField(max_length=250)
    location            =    models.CharField(max_length=250)
    email               =    models.EmailField(max_length=250, unique=True)
    password            =    models.CharField(max_length=250)
    contact_number      =    models.PositiveIntegerField(null=True, blank=True)
    profile_photo       =    models.ImageField(null=True, blank=True)
    designation         =    models.CharField(max_length=300)
    created_date        =    models.DateTimeField(auto_now_add=True)

    is_active           =    models.BooleanField(default=True)
    is_admin            =    models.BooleanField(default=False)
    is_staff            =    models.BooleanField(default=False)
    is_superuser        =    models.BooleanField(default=False)
    inactive_timestamp  =    models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return str(self.user_name)

    def has_perm (self, perm, obj=None):
       return True

    def has_module_perms (self, app_label):
       return True


class Organisation(models.Model):
    ORG_TYPE = (
        ('OPERATOR', 'Operator'),
        ('VENDOR', 'Vendor'),
    )
    org_name            =     models.CharField(max_length=250)
    org_type            =     models.CharField(max_length=250, choices=ORG_TYPE, default='OPERATOR')
    profile_photo       =     models.ImageField(null=True, blank=True)
    location            =     models.CharField(max_length=250, null=True, blank=True)
    email               =     models.EmailField(max_length=250)
    contact_number      =     models.PositiveIntegerField(null=True, blank=True)
    area_of_operation   =     models.CharField(max_length=250,null=True, blank=True)
    year_of_estb        =     models.DateField()
    about_organisation  =     models.CharField(max_length=500, null=True, blank=True)
    address             =     models.CharField(max_length=300,null=True, blank=True)
    website             =     models.URLField(max_length=300, null=True, blank=True)
    created_date        =     models.DateTimeField(auto_now_add=True)
    active              =     models.BooleanField(default=True)
    inactive_timestamp  =     models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.org_type)


class Tags(models.Model):
    item                =   models.CharField(max_length=250)
    active              =   models.BooleanField(default=True)
    org_id              =   models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='tag')
    inactive_timestamp  =   models.DateTimeField()
    created_date        =   models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.item)


class Aircraft(models.Model):
    name                =   models.CharField(max_length=250)
    year_of_manufacture =   models.CharField(max_length=250)
    manufacturer        =   models.CharField(max_length=250)
    org_id              =   models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='aircrafts')
    active              =   models.BooleanField(default=True)
    inactive_timestamp  =   models.DateTimeField()
    created_date        =   models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class OrgUser(models.Model):
    user_id            =  models.ForeignKey(Users, on_delete=models.CASCADE, related_name='orguser')
    org_id              =  models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='userorg')
    active             =  models.BooleanField(default=True)
    inactive_timestamp =  models.DateTimeField(max_length=100)
    created_time       =  models.DateField(auto_now_add=True)


class OperatorVendor(models.Model):
    orgid_opt           =      models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='Orgopt')
    orgid_vend          =      models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='vendor')
    active              =      models.BooleanField(default=True)
    inactive_timestamp  =      models.DateTimeField(max_length=100)


class OperatorVendChange(models.Model):
    optvend_map_id     =   models.ForeignKey(OperatorVendor, on_delete=models.CASCADE, related_name='operatorvendchange')
    state              =   models.BooleanField(default=True)
    created_date       =   models.DateField(auto_now_add=True)
    edited_by_user_id  =   models.ForeignKey(Users, on_delete=models.CASCADE, related_name='privatelist_change')


class Blacklisted(models.Model):
    orgid_opt          =    models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='blacklisted_by')
    orgid_vend         =    models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='blacklisteds')
    active             =    models.BooleanField(default=True)
    inactive_timestamp =    models.DateTimeField(max_length=100)

    @property
    def blacklistedChanges(self):
        return self.blacklistedChange_set.all()

class BlacklistedChange(models.Model):
    blacklisted_id     =   models.ForeignKey(Blacklisted, on_delete=models.CASCADE, related_name='blacklistedchange')
    state              =   models.BooleanField(default=True)
    created_date       =   models.DateField(auto_now_add=True)
    edited_by_user_id  =   models.ForeignKey(Users, on_delete=models.CASCADE, related_name='blacklisted_change_by')



