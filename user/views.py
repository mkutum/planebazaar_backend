from django.http import Http404, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import generics, status, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, get_object_or_404, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from PlaneBazaar.Decorators import login_required
from user.CustomAuth import IsAdminOrStaff, IsOwner, CustomAuthentication
from user.models import Users, Organisation, Tags, Aircraft, OrgUser, OperatorVendor, Blacklisted, BlacklistedChange
from user.serializers import LoginSerializer, ChangePasswordSerializer, UserSerializer, OrganisationSerializer, \
    TagsSerializer, AircraftSerializer, OrgUserSerializer, OperatorVendorSerializer, BlacklistedSerializer, \
    VendorOrgDetailsSerializer, OperatorOrgDetailsSerializer, BlacklistChangeSerializer, EmailVerifySerializer


# email verify
class EmailVerificationView(APIView):
    serializer_class = EmailVerifySerializer
    permission_classes = (IsAdminOrStaff,)

    def post (self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


# Get All Vendor List
class GetAllVendorListView(generics.ListAPIView):
    permission_classes = (CustomAuthentication,)
    serializer_class = OrganisationSerializer
    queryset = Organisation.objects.filter(org_type='VENDOR').filter(active='True')
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('org_name', 'address', 'id')
    search_fields = ('org_name', 'address', 'id')
    ordering_fields = ('org_name', 'id',)

# Get Indivisual Vendor Details
class GetIndividualVendorOrgDetails(generics.ListAPIView):
    permission_classes = (CustomAuthentication,)
    serializer_class = VendorOrgDetailsSerializer
    queryset = Organisation.objects.filter(org_type='VENDOR').filter(active='True')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ['id', ]

# Get Indivisual Operator Details
class GetIndivisualOperatorsDetails(generics.ListAPIView):
    permission_classes = (CustomAuthentication,)
    serializer_class = OperatorOrgDetailsSerializer
    queryset = Organisation.objects.filter(org_type='OPERATOR').filter(active='True')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ['id', ]

# Operator Privatelist Creation
class GetPrivateVendorList(APIView):
    @login_required
    def get (self, request, format=None):
        user = self.request.user.__getattribute__('id')  # current user_id
        orgmap_id = OrgUser.objects.filter(user_id=user)  # user org mapping id
        orgid = orgmap_id.values_list('org_id')  # get org_id
        privatevendor = OperatorVendor.objects.filter(
            orgid_opt__in=orgid).filter(
            active='True')  # filter data with org_id fro private vendor(operatorVendor) model
        serializer = OperatorVendorSerializer(privatevendor, many=True)
        return Response(serializer.data)

# Add vendor to private list
class AddVendorToPrivateList(ListCreateAPIView):
    queryset = OperatorVendor.objects.all()
    serializer_class = OperatorVendorSerializer

    @login_required
    def post (self, request, format=None):
        orguser = OrgUser.objects.filter(user_id=request.user.id)
        org_id = orguser.values_list('org_id')
        orgid = Organisation.objects.filter(id__in=org_id)
        serializer = self.serializer_class(data=request.data)  # has to pass user from OrgUser model
        if serializer.is_valid():
            serializer.save(orgid_opt=orgid[0])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Blacklisted Vendor List
class AddVendorToBlackList(generics.ListCreateAPIView):
    queryset = Blacklisted.objects.all()
    serializer_class = BlacklistedSerializer

    @login_required
    def post (self, request, format=None):
        orguser = OrgUser.objects.filter(user_id=request.user.id)
        org_id = orguser.values_list('org_id')
        orgid = Organisation.objects.filter(id__in=org_id)
        serializer = self.serializer_class(data=request.data)  # has to pass user from OrgUser model
        if serializer.is_valid():
            serializer.save(orgid_opt=orgid[0])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get Blacklisted Vendor List
class GetBlackListedVendor(APIView):

    @login_required
    def get (self, request, format=None):
        user = self.request.user.__getattribute__('id')  # current user_id
        orgmap_id = OrgUser.objects.filter(user_id=user)  # user org mapping id
        orgid = orgmap_id.values_list('org_id')  # get org_id
        blacklistvendor = Blacklisted.objects.filter(
            orgid_opt__in=orgid).filter(active=True)  # filter data with org_id fro private vendor(operatorVendor) model
        serializer = BlacklistedSerializer(blacklistvendor, many=True)
        return Response(serializer.data)

# Search Vendor Org details by feilds
class SearchVendorbyFields(generics.ListAPIView):
    serializer_class = OrganisationSerializer
    queryset = Organisation.objects.filter(org_type='VENDOR')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ['id', 'org_name', 'address']

# Login API
class LoginView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = LoginSerializer

    def post (self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class LogoutView(APIView):
    def post (self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout Successful.'
        }
        return response

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = Users

    def get_object (self, queryset=None):
        obj = self.request.user
        return obj

    def update (self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        # if not request.user.is_authenticated:
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Add new Users
class UserCreationView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()
    permission_classes = (IsAdminOrStaff,)


# Has to check permission parts
class UpdateUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()
    permission_classes = (IsAdminOrStaff, IsOwner,)

    def get_object(self, pk):
        try:
            return Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            raise Http404


    """def get_object (self, pk):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))
        if self.check_object_permissions(self.request, obj):
            return obj
        else:
            raise Http404()"""

    def get (self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserSerializer(snippet)
        return Response(serializer.data)

    def put (self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete (self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Add new Aircraft Details
class AircraftCreationView(generics.ListCreateAPIView):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    permission_classes = (IsAdminOrStaff,)

    @login_required
    def post (self, request, format=None):
        orguser = OrgUser.objects.filter(user_id=request.user.id)
        org_id = orguser.values_list('org_id')
        orgid = Organisation.objects.filter(id__in=org_id)
        serializer = self.serializer_class(data=request.data)  # has to pass user from OrgUser model
        if serializer.is_valid():
            serializer.save(org_id=orgid[0])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAircraftView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    permission_classes = (IsAdminOrStaff,)


# Add new Organisations Details
class OrgCreationListView(generics.ListCreateAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = (AllowAny,)


class UpdateOrgView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = (AllowAny,)


# Add new Tags Details
class TagsCreationView(generics.ListCreateAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (AllowAny,)


class UpdateTagsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (AllowAny,)



# Org User Mapping Creation
class OrgUserCreationListView(generics.ListCreateAPIView):
    queryset = OrgUser.objects.all()
    serializer_class = OrgUserSerializer
    permission_classes = (AllowAny,)


class UpdateOrgUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrgUser.objects.all()
    serializer_class = OrgUserSerializer
    permission_classes = (AllowAny,)

# Blacklisted Change Creation
class BlacklistChangeCreationListView(generics.ListCreateAPIView):
    queryset = BlacklistedChange.objects.all()
    serializer_class = BlacklistChangeSerializer

    @login_required
    def post (self, request, format=None):
        orguser = OrgUser.objects.filter(user_id=request.user.id)
        org_id = orguser.values_list('org_id')
        orgid = Organisation.objects.filter(id__in=org_id)
        serializer = self.serializer_class(data=request.data)  # has to pass user from OrgUser model
        if serializer.is_valid():
            serializer.save(edited_by_user_id=orgid[0])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# User Log Details

def GetLogDetailsView(self):
    return HttpResponse('User Log Details Page..')