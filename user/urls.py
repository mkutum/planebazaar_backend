from django.urls import path

from user import views

urlpatterns = [
    # Admin Api's
    path('Login/', views.LoginView.as_view(), name='login'),
    path('Logout/', views.LogoutView.as_view(), name='logout'),
    path('ChangePassword/', views.ChangePasswordView.as_view(), name='logout'),

    path('EmailVerify/', views.EmailVerificationView.as_view(), name='Email_verify'),
    path('signup/', views.OrgCreationListView.as_view(), name='Organisation_creations'),
    path('UpdateOrganisationProfile/<int:pk>/', views.UpdateOrgView.as_view(), name='Update_Organisation_details'),

    path('CreateUser/', views.UserCreationView.as_view(), name='User_creations'),
    path('UpdateUser/<int:pk>/', views.UpdateUserView.as_view(), name='Update_user_details'),

    path('CreateAircraft/', views.AircraftCreationView.as_view(), name='Aircraft_creations'),
    path('UpdateAircraft/<int:pk>/', views.UpdateAircraftView.as_view(), name='Update_Aircraft_details'),

    path('GetLogDetails/', views.GetLogDetailsView, name = 'Get_user_log_details'),

    # Vendor Management Apis
    path('GetAllVendorList/', views.GetAllVendorListView.as_view(), name='Get_all_VendorList'),
    path('AddVendorToPrivateList/', views.AddVendorToPrivateList.as_view(), name='Add_vendor_Privatelist'),
    path('AddVendorToBlackList/', views.AddVendorToBlackList.as_view(), name='Add_vendor_Blacklist'),
    path('GetBlackListVendor/', views.GetBlackListedVendor.as_view(), name='Get_Blacklist_vendor'),
    path('GetPrivateVendorList/', views.GetPrivateVendorList.as_view(), name='Get_Private_vendor_list'),
    path('SearchVendorList/', views.SearchVendorbyFields.as_view(), name='Search_vendor_by_fields'),
    path('GetIndividualVendorDetails/', views.GetIndividualVendorOrgDetails.as_view(), name='Vendor_org_details'),
    path('GetIndividualOperatorsDetails/', views.GetIndivisualOperatorsDetails.as_view(), name='Operator_org_details'),


    path('CreateTags/', views.TagsCreationView.as_view(), name='Tags_creations'),
    path('UpdateOrganisationProfile/<int:pk>/', views.UpdateTagsView.as_view(), name='Update_Tags_details'),
    path('CreateOrgUserMapping/', views.OrgUserCreationListView.as_view(), name='OrgUserMapping_creations'),
    path('UpdateOrgUserMapping/<int:pk>/', views.UpdateOrgUserView.as_view(), name='Update_OrgUserMapping_details'),
]

