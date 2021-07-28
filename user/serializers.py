from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import *

User = get_user_model()


def get_tokens_for_user (user):
    refresh = RefreshToken.for_user(user)


    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=500, read_only=True)

    def validate (self, data):

        email = data.get('email')
        password = data.get('password')

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        if user.is_active:
            token = get_tokens_for_user(user)

        return {
            'email': user.email,
            'token': token,
        }


class ChangePasswordSerializer(serializers.Serializer):
    class Meta:
        model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

    def create (self, validate_data):
        password = validate_data.pop('password', None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = (
            'id', 'org_name', 'org_type', 'profile_photo', 'area_of_operation', 'year_of_estb', 'about_organisation',
            'address', 'website', 'created_date', 'active')


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'
        read_only_fields = ('org_id',)


class OrgUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgUser
        fields = '__all__'
        depth = 2


class OperatorVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatorVendor
        fields = '__all__'
        read_only_fields = ('orgid_opt',)
        depth = 2


class OptVendChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatorVendChange
        fields = '__all__'


class BlacklistChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlacklistedChange
        fields = '__all__'
        read_only_fields = ('edited_by_user_id', 'blacklisted_id')


class BlacklistedSerializer(serializers.ModelSerializer):
    blacklistchanges = BlacklistChangeSerializer(many=True)

    class Meta:
        model = Blacklisted
        fields = '__all__'
        read_only_fields = ('orgid_opt',)
        depth = 2

    def create (self, validated_data):
        blacklistchanges = validated_data.pop('blacklistchanges')
        blacklist = Blacklisted.objects.create(**validated_data)
        for blacklistchange in blacklistchanges:
            BlacklistedChange.objects.create(**blacklistchange, blacklisted_id=blacklist)
        return blacklist


class VendorOrgDetailsSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField('get_tags')
    users = serializers.SerializerMethodField('get_users')

    def get_tags (self, org_id):
        tags = Tags.objects.filter(org_id=org_id)
        serializer = TagsSerializer(instance=tags, many=True)
        return serializer.data

    def get_users (self, org_id):
        user = OrgUser.objects.filter(org_id=org_id)
        users = user.values_list('user_id')
        allusers = Users.objects.filter(id__in=users)
        serializer = UserSerializer(instance=allusers, many=True)
        return serializer.data

    class Meta:
        model = Organisation
        fields = (
            'id', 'org_name', 'org_type', 'profile_photo', 'area_of_operation', 'year_of_estb', 'about_organisation',
            'address', 'website', 'created_date', 'active', 'tags', 'users')


class OperatorOrgDetailsSerializer(serializers.ModelSerializer):
    aircrafts = serializers.SerializerMethodField('get_aircrafts')
    users = serializers.SerializerMethodField('get_users')

    def get_aircrafts (self, org_id):
        aircrafts = Aircraft.objects.filter(org_id=org_id)
        serializer = AircraftSerializer(instance=aircrafts, many=True)
        return serializer.data

    def get_users (self, org_id):
        user = OrgUser.objects.filter(org_id=org_id)
        users = user.values_list('user_id')
        allusers = Users.objects.filter(id__in=users)
        serializer = UserSerializer(instance=allusers, many=True)
        return serializer.data

    class Meta:
        model = Organisation
        fields = (
            'id', 'org_name', 'org_type', 'profile_photo', 'area_of_operation', 'year_of_estb', 'about_organisation',
            'address', 'website', 'created_date', 'active', 'aircrafts', 'users')


# email verification serializer
class EmailVerifySerializer(serializers.ModelSerializer):
    #email = serializers.CharField(max_length=255)

    class Meta:
        model = Users
        fields = ('email',)
