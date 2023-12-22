from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import HTTP_HEADER_ENCODING, viewsets, permissions, status
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import action
from .views_helper import *
import json
from django.http import JsonResponse, request, response
from rest_framework.views import APIView
from pathlib import Path
from .object import Task
from django.http import Http404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.user.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.user.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.user.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.user.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.user.delete')
        return super().get_permissions()

    def list(self, request):
        results = self.queryset.filter(profile__status=True)
        serializer = UserSerializer(results, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        profile = Profile.objects.get(user_id=pk)
        serializer = UserSerializer(profile)
        if serializer.is_valid:
            profile.status = False
            profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AfpViewSet(viewsets.ModelViewSet):
    queryset = Afp.objects.filter()
    serializer_class = AfpSerializer

    def get_queryset(self):
        return super().get_queryset()

    def destroy(self, request, pk=None):
        afp = Afp.objects.get(pk=pk)
        ManageRequest.delete_request(pk, afp.fk_processid)
        afp.status = 0
        afp.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class ApiLogViewSet(viewsets.ModelViewSet):
    queryset = ApiLog.objects.all()
    serializer_class = ApiLogSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ApprovalStageViewSet(viewsets.ModelViewSet):
    queryset = ApprovalStage.objects.all()
    serializer_class = ApprovalStageSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.branch.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.branch.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.branch.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.branch.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.branch.delete')
        return super().get_permissions()


class BranchDepartmentViewSet(viewsets.ModelViewSet):
    queryset = BranchDepartment.objects.all()
    serializer_class = BranchDepartmentSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.branch.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.branch.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.branch.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.branch.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.branch.delete')
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.get_branch_departments(
            self, queryset, self.request.query_params.get('branchId'), self.request.query_params.get('department_id'))
        return data


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.department.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.department.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.department.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.department.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.department.delete')
        return super().get_permissions()


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.newemployees.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.newemployee.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.newemployee.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.newemployee.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.newemployee.delete')
        return super().get_permissions()


class ExpenseSheetViewSet(viewsets.ModelViewSet):
    queryset = ExpenseSheet.objects.filter()
    serializer_class = ExpenseSheetSerializer

    def destroy(self, request, pk=None):
        expense_sheet = ExpenseSheet.objects.get(pk=pk)
        ManageRequest.delete_request(pk, expense_sheet.fk_processid)
        expense_sheet.status = 0
        expense_sheet.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class FinancialYearViewSet(viewsets.ModelViewSet):
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer


class FuelRequestViewSet(viewsets.ModelViewSet):
    queryset = FuelRequest.objects.all()
    serializer_class = FuelRequestSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.filter()
    serializer_class = ProcessSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.query_params.get('category_id') is not None:
            queryset = ViewsHelper.get_process_category(
                self, queryset, self.request.query_params.get('category_id'))

        if self.request.query_params.get('process_code') is not None:
            queryset = ViewsHelper.filter_by_process_code(
                self, queryset, self.request.query_params.get('process_code'))
        return queryset

    def destroy(self, request, pk):
        process = Process.objects.get(pk_processid=pk)
        # raise APIException(profile)
        serializer = ProcessSerializer(process)
        if serializer.is_valid:
            process.status = 0
            process.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProcessCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProcessCategory.objects.all()
    serializer_class = ProcessCategorySerializer


class ProfileRoleViewSet(viewsets.ModelViewSet):
    queryset = ProfileRole.objects.all()
    serializer_class = ProfileRoleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.get_profile_roles(
            self, queryset, self.request.query_params.get('profileId'), self.request.query_params.get('role_id'))
        return data


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.get_profile(
            self, queryset, self.request.query_params.get('user_id'))
        return data


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer

    @action(detail=False, methods=['POST'])
    def bulk_delete(self, request, pk=None):
        for id in request.data['ids']:
            try:
                RolePermission.objects.filter(pk_role_permissionid=id).delete()
            except:
                pass
        return Response(True)

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset.filter(
            fk_roleid=self.request.query_params.get('fk_roleid'))
        return data


class SystemConfigViewSet(viewsets.ModelViewSet):
    queryset = SystemConfig.objects.all()
    serializer_class = SystemConfigSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.get_config(
            self, queryset)
        return data


class HelpTopicViewSet(viewsets.ModelViewSet):
    queryset = HelpTopic.objects.all()
    serializer_class = HelpTopicSerializer


class HelpdeskViewSet(viewsets.ModelViewSet):
    queryset = Helpdesk.objects.all()
    serializer_class = HelpdeskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('user'):
            queryset = Helpdesk.objects.filter(
                fk_profileid__user__id=self.request.user.id)
        return queryset


class HelpdeskStatusViewSet(viewsets.ModelViewSet):
    queryset = IssueStatus.objects.all()
    serializer_class = HelpdeskStatusSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.get_helpdesk_status(
            self, queryset, self.request.query_params.get('helpdesk_id'))
        return data


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.projects.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.project.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.project.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.project.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.project.delete')
        return super().get_permissions()


class AssetTypeViewSet(viewsets.ModelViewSet):
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerializer


class GocViewSet(viewsets.ModelViewSet):
    queryset = Goc.objects.filter()
    serializer_class = GocSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return super().get_queryset()

    def destroy(self, request, pk=None):
        goc = Goc.objects.get(pk=pk)
        ManageRequest.delete_request(pk, goc.fk_processid)
        goc.status = 0
        goc.save()
        return Response({'status': ''}, status=status.HTTP_404_NOT_FOUND)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.filter()
    serializer_class = VendorSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.vendors.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.vendor.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.vendor.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.vendor.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.vendor.delete')
        return super().get_permissions()

    def destroy(self, request, pk=None):
        vendor = Vendor.objects.get(pk=pk)
        ManageRequest.delete_request(pk, vendor.fk_processid)
        vendor.status = 0
        vendor.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class PayableWaiverViewSet(viewsets.ModelViewSet):
    queryset = PayableWaiver.objects.filter()
    serializer_class = PayableWaiverSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.payablewaivers.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.payablewaiver.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.payablewaiver.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.payablewaiver.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.payablewaiver.delete')
        return super().get_permissions()

    def destroy(self, request, pk=None):
        payable_waiver = PayableWaiver.objects.get(pk=pk)
        ManageRequest.delete_request(pk, payable_waiver.fk_processid)
        payable_waiver.status = 0
        payable_waiver.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class NewEmployeeViewSet(viewsets.ModelViewSet):
    queryset = NewEmployee.objects.filter()
    serializer_class = NewEmployeeSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.newemployees.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.newemployee.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.newemployee.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.newemployee.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.newemployee.delete')
        return super().get_permissions()

    def destroy(self, request, pk=None):
        new_employee = NewEmployee.objects.get(pk=pk)
        ManageRequest.delete_request(pk, new_employee.fk_processid)
        new_employee.status = 0
        new_employee.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class StationeryTypeViewSet(viewsets.ModelViewSet):
    queryset = StationeryType.objects.all()
    serializer_class = StationeryTypeSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.stationery.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.stationery.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.stationery.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.stationery.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.stationery.delete')
        return super().get_permissions()


class StationeryViewSet(viewsets.ModelViewSet):
    queryset = Stationery.objects.filter()
    serializer_class = StationerySerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.stationeryrequests.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.stationeryrequest.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.stationeryrequest.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.stationeryrequest.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.stationeryrequest.delete')
        return super().get_permissions()

    def destroy(self, request, pk=None):
        stationery = Stationery.objects.get(pk=pk)
        ManageRequest.delete_request(pk, stationery.fk_processid)
        stationery.status = 0
        stationery.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class StationeryDetailsViewSet(viewsets.ModelViewSet):
    queryset = StationeryDetail.objects.all()
    serializer_class = StationeryDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.filter_stationery(
            self, queryset, self.request.query_params.get('fk_stationeryid'))
        return data


class MileageViewSet(viewsets.ModelViewSet):
    queryset = Mileage.objects.all()
    serializer_class = MileageSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.mileages.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.mileage.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.mileage.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.mileage.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.mileage.delete')
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.filter_mileage_vehicle(
            self, queryset, self.request.query_params.get('fk_vehicleid'))
        return data


class MileageDetailsViewSet(viewsets.ModelViewSet):
    queryset = MileageDetail.objects.all()
    serializer_class = MileageDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.filter_Mileage(
            self, queryset, self.request.query_params.get('fk_mileageid'))
        return data


class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.filter_voucher(
            self, queryset, self.request.query_params.get('fk_expense_sheetid'))
        return data


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class NatureMovementViewSet(viewsets.ModelViewSet):
    queryset = NatureMovement.objects.all()
    serializer_class = NatureMovementSerializer


class AssetMovementViewSet(viewsets.ModelViewSet):
    queryset = AssetMovement.objects.filter()
    serializer_class = AssetMovementSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.movedassets.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.movedasset.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.movedasset.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.movedasset.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.movedasset.delete')
        return super().get_permissions()

    def destroy(self, request, pk=None):
        asset_movement = AssetMovement.objects.get(pk=pk)
        ManageRequest.delete_request(pk, asset_movement.fk_processid)
        asset_movement.status = 0
        asset_movement.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class SapRightsViewSet(viewsets.ModelViewSet):
    queryset = SapRights.objects.filter()
    serializer_class = SapRightsSerializer

    def destroy(self, request, pk=None):
        sap_right = SapRights.objects.get(pk=pk)
        ManageRequest.delete_request(pk, sap_right.fk_processid)
        sap_right.status = 0
        sap_right.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class OvertimeViewSet(viewsets.ModelViewSet):
    queryset = Overtime.objects.filter()
    serializer_class = OvertimeSerializer

    def destroy(self, request, pk=None):
        overtime = Overtime.objects.get(pk=pk)
        ManageRequest.delete_request(pk, overtime.fk_processid)
        overtime.status = 0
        overtime.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class OvertimeDetailViewSet(viewsets.ModelViewSet):
    queryset = OvertimeDetail.objects.all()
    serializer_class = OvertimeDetailSerializer


class AssetDisposalViewSet(viewsets.ModelViewSet):
    queryset = AssetDisposal.objects.all()
    serializer_class = AssetDisposalSerializer


class OvertimeDetailsViewSet(viewsets.ModelViewSet):
    queryset = OvertimeDetail.objects.all()
    serializer_class = OvertimeDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.filter_overtime(
            self, queryset, self.request.query_params.get('fk_overtimeid'))
        return data


class WorkFlowRightsViewSet(viewsets.ModelViewSet):
    queryset = WorkflowRights.objects.filter()
    serializer_class = WorkFlowRightsSerializer

    def destroy(self, request, pk=None):
        workflow_right = WorkflowRights.objects.get(pk=pk)
        ManageRequest.delete_request(pk, workflow_right.fk_processid)
        workflow_right.status = 0
        workflow_right.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class TravelViewSet(viewsets.ModelViewSet):
    queryset = Travel.objects.filter()
    serializer_class = TravelSerializer

    def destroy(self, request, pk=None):
        travel = Travel.objects.get(pk=pk)
        ManageRequest.delete_request(pk, travel.fk_processid)
        travel.status = 0
        travel.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class ProcessApprovalStageViewSet(viewsets.ModelViewSet):
    queryset = ProcessApprovalStage.objects.all()
    serializer_class = ProcessApprovalStageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.get_process_approval_stages(
            self, queryset, self.request.query_params.get('fk_processid'))
        return data


class ApprovalRoleViewSet(viewsets.ModelViewSet):
    queryset = ApprovalRole.objects.all()
    serializer_class = ApprovalRoleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.get_process_approval_roles(
            self, queryset, self.request.query_params.get('process_id'), self.request.query_params.get('status'))
        return data


class DeleteProcessApprovalStageViewSet(viewsets.ModelViewSet):
    queryset = ProcessApprovalStage.objects.all()
    serializer_class = ProcessApprovalStageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.delete_process_approval_stage(
            self, queryset, self.request.query_params.get('delete_stage'))
        return data


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.filter()
    serializer_class = RequestSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        processCode = self.request.query_params.get('process_code')
        user_id = self.request.query_params.get('user_id')

        if processCode is not None:
            try:
                process = Process.objects.get(process_code=processCode)
                return queryset.filter(fk_processid=process.pk_processid)
            except:
                return []
        if user_id is not None:
            try:
                profile = Profile.objects.get(user=user_id)
                return queryset.filter(fk_profileid=profile.pk_profileid)
            except Profile.DoesNotExist:
                return []

        data = ViewsHelper.get_request_workflowid_process(self, queryset, self.request.query_params.get(
            'fk_processid'), self.request.query_params.get('workflowid'))
        return data

    def destroy(self, request, pk=None):
        request = Request.objects.get(pk=pk)
        request.status = 0
        request.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class GOCAmountViewSet(viewsets.ModelViewSet):
    queryset = GocAmount.objects.all()
    serializer_class = GOCAmountSerializer


class ProcessStageApproverViewSet(viewsets.ModelViewSet):
    queryset = ProcessStageApprover.objects.filter(approver_status='active')
    serializer_class = ProcessStageApproverSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.get_process_stage_approvers(
            self, queryset, self.request.query_params.get('process_id'))
        return data


class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.get_approval(
            self, queryset, self.request.query_params.get('requestId'))
        return data


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.get_active_notifications(
            self, queryset, self.request.query_params.get('profileId'))
        return data


class ResetPasswordViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     password = SerializerHelper.random_password(self)
    #     for user in queryset:
    #         user = User.objects.get(username=user)
    #         user.password = make_password(password)
    #         user.save()
    #         DataPointMailer.password_reset(user, password)
    #     return queryset


class ProfileRolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.get_profile_role_permissions(
            self, queryset, self.request.query_params.get('profile_id'), self.request.query_params.get('permission_code'))
        return data


class SystemBackupViewSet(viewsets.ModelViewSet):
    queryset = SystemBackup.objects.all()
    serializer_class = SystemBackUpSerializer

    def destroy(self, request, *args, **kwargs):
        backup = self.get_object()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(BASE_DIR, 'backups/' + backup.backup_file.strip())
        if os.path.exists(path):
            os.remove(path)
        backup.delete()
        return Response(True)


class ManualJournalRequestViewSet(viewsets.ModelViewSet):
    queryset = ManualJournalRequest.objects.all()
    serializer_class = ManualJournalRequestSerializer

    def get_permissions(self):
        if self.action == 'list':
            Security.SecureAccess(self, 'system.movedassets.view')
        elif self.action == 'retrieve':
            Security.SecureAccess(self, 'system.movedasset.manage')
        elif self.action == 'create':
            Security.SecureAccess(self, 'system.movedasset.add')
        elif self.action == 'update' or self.action == 'partial_update':
            Security.SecureAccess(self, 'system.movedasset.manage')
        elif self.action == 'destroy':
            Security.SecureAccess(self, 'system.movedasset.delete')
        return super().get_permissions()

    def destroy(self, request, pk=None):
        manual_journal_request = ManualJournalRequest.objects.get(pk=pk)
        ManageRequest.delete_request(pk, manual_journal_request.fk_processid)
        manual_journal_request.status = 0
        manual_journal_request.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class ManualJournalRequestDetailViewSet(viewsets.ModelViewSet):
    queryset = ManualJournalRequestDetail.objects.all()
    serializer_class = ManualJournalRequestDetailSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class ProfileDepartmentViewSet(viewsets.ModelViewSet):
    queryset = ProfileDepartment.objects.all()
    serializer_class = ProfileDepartmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.get_profile_departments(
            self, queryset, self.request.query_params.get('profileId'), self.request.query_params.get('department_id'))
        return data


class UserPermissionViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = RolePermission.objects.all()

    def list(self, request):
        roles = ProfileRole.objects.filter(
            fk_profileid__user_id=self.request.user.id)
        queryset = set()
        for role in roles:
            queryset = queryset.union(
                self.queryset.filter(fk_roleid=role.fk_roleid))

        serializer = RolePermissionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        role = ProfileRole.objects.get(fk_profileid__user_id=pk)
        queryset = self.queryset.filter(fk_roleid=role.fk_roleid)

        serializer = RolePermissionSerializer(queryset, many=True)
        return Response(serializer.data)


class UserRequestViewSet(viewsets.ViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class ManageRequest():
    def delete_request(workflowid, processid):
        request = Request.objects.get(
            workflow_id=workflowid, fk_processid=processid)
        request.status = 0
        return


class HelpdeskFileViewSet(viewsets.ModelViewSet):
    queryset = HelpdeskFile.objects.all()
    serializer_class = HelpdeskFileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('helpdeskid'):
            queryset = HelpdeskFile.objects.filter(
                fk_helpdeskid=self.request.query_params.get('helpdeskid'))
        return queryset


class HandoverViewSet(viewsets.ModelViewSet):
    queryset = Handover.objects.all()
    serializer_class = HandoverSerializer

class CardAccountLoadingViewSet(viewsets.ModelViewSet):
    queryset = Cal.objects.filter()
    serializer_class = CardAccountLoadingSerializer

    def destroy(self, request, pk=None):
        cal = Cal.objects.get(pk=pk)
        ManageRequest.delete_request(pk, cal.fk_processid)
        cal.status = 0
        cal.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)  

class CardLoadItemsViewSet(viewsets.ModelViewSet):
    queryset = CardItem.objects.all()
    serializer_class = CardLoadItemsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.filter_cal(
            self, queryset, self.request.query_params.get('fk_cal_id'))
        return data    

class CardCreateViewSet(viewsets.ModelViewSet):
    queryset = Cao.objects.filter()
    serializer_class = CardCreateSerializer

    def destroy(self, request, pk=None):
        cao = Cao.objects.get(pk=pk)
        ManageRequest.delete_request(pk, cao.fk_processid)
        cao.status = 0
        cao.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)  

class CardCreateItemsViewSet(viewsets.ModelViewSet):
    queryset = CardCreateItem.objects.all()
    serializer_class = CardCreateItemsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.filter_cao(
            self, queryset, self.request.query_params.get('fk_cao_id'))
        return data    


class CacViewSet(viewsets.ModelViewSet):
    queryset = Cac.objects.filter()
    serializer_class = CacSerializer

    def destroy(self, request, pk=None):
        cac = Cac.objects.get(pk=pk)
        ManageRequest.delete_request(pk, cac.fk_processid)
        cac.status = 0
        cac.save()
        return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)  



class CacProductViewSet(viewsets.ModelViewSet):
    queryset = CacProduct.objects.all()
    serializer_class = CacProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.filter_cac(
            self, queryset, self.request.query_params.get('fk_cac_id'))
        return data   


class CacLubricantViewSet(viewsets.ModelViewSet):
    queryset = CacLubricant.objects.all()
    serializer_class = CacLubricantSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        data = ViewsHelper.filter_cac(
            self, queryset, self.request.query_params.get('fk_cac_id'))
        return data               


class Security():
    def SecureAccess(self, code):
        return
        profile = SerializerHelper.get_profile_id(
            self, self.request.user.id)
        roles = ProfileRole.objects.filter(
            fk_profileid_id=profile.pk_profileid)
        permission = Permission.objects.get(permission_code=code)

        for role in roles:
            try:
                role_permission = RolePermission.objects.get(
                    fk_permissionid=permission.pk_permissionid, fk_roleid=role.fk_roleid)
                if role_permission:
                    return
            except RolePermission.DoesNotExist:
                pass
        return
        raise APIException(
            'You do not have permission to perform this action.')
class ProjectRequestViewSet(viewsets.ModelViewSet):
    queryset = ProjectRequest.objects.all()
    serializer_class = ProjectRequestSerializer

class ProjectStakeholderViewSet(viewsets.ModelViewSet):
    queryset = ProjectStakeholder.objects.all()
    serializer_class = ProjectStakeholderSerializer

class ProjectMilestoneViewSet(viewsets.ModelViewSet):
    queryset = ProjectMilestone.objects.all()
    serializer_class = ProjectMilestoneSerializer
    
class ProjectStaffResViewSet(viewsets.ModelViewSet):
    queryset = ProjectStaffRes.objects.all()
    serializer_class = ProjectStaffResSerializer
