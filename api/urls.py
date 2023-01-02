from django.conf.urls import url, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
import datapoint.views as views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Datapoint API",
        default_version='v2',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='User')

router.register(
    r'user_profiles',
    views.UserProfileViewSet,
    basename='User Profiles')

router.register(r'afps', views.AfpViewSet, basename='AFP')

router.register(r'api_logs', views.ApiLogViewSet, basename='API Logs')

router.register(r'currencies', views.CurrencyViewSet, basename='Currencies')

router.register(
    r'approval_stages',
    views.ApprovalStageViewSet,
    basename='Approval Stages')

router.register(r'branches', views.BranchViewSet, basename='Branches')

router.register(
    r'branch_departments',
    views.BranchDepartmentViewSet,
    basename='Branch Department')

router.register(r'departments', views.DepartmentViewSet, basename='Department')

router.register(r'employees', views.EmployeeViewSet, basename='Employees')

router.register(
    r'expense_sheets',
    views.ExpenseSheetViewSet,
    basename='Expense Sheets')

router.register(
    r'financial_years',
    views.FinancialYearViewSet,
    basename='Financial Years')

router.register(
    r'fuels',
    views.FuelRequestViewSet,
    basename='Fuel Requests')

router.register(
    r'permissions',
    views.PermissionViewSet,
    basename='Permissions')

router.register(r'processes', views.ProcessViewSet, basename='Processes')

router.register(
    r'process_spproval_stages',
    views.ProcessApprovalStageViewSet,
    basename='Process Approval Stages')

router.register(
    r'process_categories',
    views.ProcessCategoryViewSet,
    basename='Process Category')

router.register(
    r'profile_roles',
    views.ProfileRoleViewSet,
    basename='Profile Roles')

router.register(r'profiles', views.ProfileViewSet, basename='Profiles')

router.register(r'roles', views.RoleViewSet, basename='Roles')

router.register(
    r'role_permissions',
    views.RolePermissionViewSet,
    basename='Role Permissions')

router.register(
    r'system_configs',
    views.SystemConfigViewSet,
    basename='System Configs')

router.register(r'help_topics', views.HelpTopicViewSet, basename='Help Topics')

router.register(r'helpdesks', views.HelpdeskViewSet, basename='Helpdesk')

router.register(
    r'helpdesk_status',
    views.HelpdeskStatusViewSet,
    basename='Helpdesk Status')

router.register(
    r'projects',
    views.ProjectViewSet,
    basename='Projects')


router.register(
    r'asset_types',
    views.AssetTypeViewSet,
    basename='Asset Types')


router.register(
    r'gocs',
    views.GocViewSet,
    basename='Grant of Credits')

router.register(
    r'vendors',
    views.VendorViewSet,
    basename='Vendors')

router.register(
    r'payable_waivers',
    views.PayableWaiverViewSet,
    basename='Payable Waivers')

router.register(
    r'new_employees',
    views.NewEmployeeViewSet,
    basename='New Employees')

router.register(
    r'stationery_types',
    views.StationeryTypeViewSet,
    basename='Stationery Types')

router.register(
    r'stationery',
    views.StationeryViewSet,
    basename='Stationery')

router.register(
    r'stationary_details',
    views.StationeryDetailsViewSet,
    basename='Stationery Details')

router.register(
    r'mileage_details',
    views.MileageDetailsViewSet,
    basename='Mileage Details')

router.register(
    r'mileages',
    views.MileageViewSet,
    basename='Mileages')

router.register(
    r'vouchers',
    views.VoucherViewSet,
    basename='voucher')

router.register(
    r'stations',
    views.StationViewSet,
    basename='station'
)

router.register(
    r'nature_movements',
    views.NatureMovementViewSet,
    basename='Nature Movement'
)
router.register(
    r'asset_movements',
    views.AssetMovementViewSet,
    basename='Asset Movement'
)
router.register(
    r'assets',
    views.AssetViewSet,
    basename='Asset'
)

router.register(
    r'sap_rights',
    views.SapRightsViewSet,
    basename='SAP Rights')

router.register(
    r'equipments',
    views.EquipmentViewSet,
    basename='IS Equipments')

router.register(
    r'overtime_details',
    views.OvertimeDetailsViewSet,
    basename='Overtime Details')

router.register(
    r'overtimes',
    views.OvertimeViewSet,
    basename='Overtime'
)

router.register(
    r'overtime_details',
    views.OvertimeDetailViewSet,
    basename='Overtime Details'
)
router.register(
    r'asset_disposals',
    views.AssetDisposalViewSet,
    basename='Asset disposal'
)

router.register(
    r'workflow_rights',
    views.WorkFlowRightsViewSet,
    basename='Workflow Rights'
)

router.register(
    r'travels',
    views.TravelViewSet,
    basename='Travel'
)

router.register(
    r'process_approval_stages',
    views.ProcessApprovalStageViewSet,
    basename='Process Approval Stages'
)

router.register(
    r'approval_roles',
    views.ApprovalRoleViewSet,
    basename='Approval Roles'
)

router.register(
    r'delete_approval_stages',
    views.DeleteProcessApprovalStageViewSet,
    basename='Delete Approval Stages'
)


router.register(
    r'requests',
    views.RequestViewSet,
    basename='Requests'
)

router.register(
    r'files',
    views.FileViewSet,
    basename='File'
)

router.register(
    r'goc_amount',
    views.GOCAmountViewSet,
    basename='GOC Amount'
)

router.register(
    r'process_stage_approvers',
    views.ProcessStageApproverViewSet,
    basename='Process Stage Approvers'
)

router.register(
    r'approvals',
    views.ApprovalViewSet,
    basename='Approvals'
)

router.register(
    r'notifications',
    views.NotificationViewSet,
    basename='Notifications'
)

router.register(
    r'profile_role_permissions',
    views.ProfileRolePermissionViewSet,
    basename='Profile Role Permissions'
)

router.register(
    r'system_backups',
    views.SystemBackupViewSet,
    basename='System Backup'
)
router.register(
    r'manual_journal_request',
    views.ManualJournalRequestViewSet,
    basename='Manual Journal Request'
)

router.register(
    r'manual_journal_request_detail',
    views.ManualJournalRequestDetailViewSet,
    basename='Manual Journal Request Detail'
)

router.register(
    r'vehicles',
    views.VehicleViewSet,
    basename='Vehicles'
)

router.register(
    r'profile_departments',
    views.ProfileDepartmentViewSet,
    basename='Profile Department')

router.register(
    r'user_permissions',
    views.UserPermissionViewSet,
    basename='User Permissionss')

router.register(
    r'user_requests',
    views.UserRequestViewSet,
    basename='User requests')

router.register(
    r'reset_password',
    views.ResetPasswordViewSet,
    basename='Rest Password')

router.register(
    r'helpdesk_files',
    views.HelpdeskFileViewSet,
    basename='Helpdesk File'
)

router.register(
    r'handover',
    views.HandoverViewSet,
    basename='Handover'
)

router.register(
    r'cals',
    views.CardAccountLoadingViewSet,
    basename='Return all card account loadings')

router.register(
    r'card_load_items',
    views.CardLoadItemsViewSet,
    basename='Fetched by fk_cal_id similar to expense sheet')    

router.register(
    r'caos',
    views.CardCreateViewSet,
    basename='Return all card account openings')

router.register(
    r'card_create_items',
    views.CardCreateItemsViewSet,
    basename='Fetched by fk_cao_id similar to expense sheet')  

router.register(
    r'cacs',
    views.CacViewSet,
    basename='Return all card account customizations')  

router.register(
    r'cac_products',
    views.CacProductViewSet,
    basename='Fetched by fk_cac_id')      

router.register(
    r'cac_lubricants',
    views.CacLubricantViewSet,
    basename='Fetched by fk_cac_id')             

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),
    # url('^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', obtain_jwt_token),
    url(r'^api/auth-refresh/', refresh_jwt_token),
    url(r'^api/auth-verify/', verify_jwt_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^redoc/$', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
