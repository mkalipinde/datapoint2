from sys import api_version
from django.contrib.auth.models import User
from django.core.checks.messages import Error
from django.http.response import HttpResponse, JsonResponse
from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.exceptions import APIException
from .models import *
from .serializer_helper import *
from datetime import datetime
from rest_framework.response import Response
from .email_service import DataPointMailer
from django.http import Http404
from io import StringIO
import os
import subprocess as sp
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.db.models import Sum
from django.contrib.auth.hashers import make_password
from django.db.models.functions import Coalesce
from .test_data import data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('__all__')
        read_only_fields = ['status']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    userprofile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'username', 'password', 'userprofile')

    def create(self, validated_data, instance=None):
        profile_data = validated_data.pop('userprofile')
        password = validated_data.pop('password')
        validated_data['is_active'] = 1
        validated_data['is_staff'] = 1

        raw_password = SerializerHelper.random_password(self)
        if password != '0':
            raw_password = password

        password = make_password(raw_password)
        user = User.objects.create_user(password=password, **validated_data)
        user.save()
        Profile.objects.update_or_create(user=user, **profile_data)
        DataPointMailer.add_user(self, validated_data.get(
            'username'), raw_password, validated_data.get('email'), validated_data.get('first_name'))
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile')
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        if validated_data.get('password') != '0':
            instance.password = make_password(validated_data.get(
                'password', instance.password))

        instance.save()
        Profile.objects.filter(user=instance).update(**profile_data)
        return instance


class ProcessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessCategory
        fields = ('__all__')


class ProcessSerializer(serializers.ModelSerializer):
    process_categoryid = ProcessCategorySerializer(
        source='fk_process_categoryid', read_only=True)

    class Meta:
        model = Process
        fields = ('__all__')


class ApiLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiLog
        fields = ('__all__')


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('__all__')


class AfpSerializer(serializers.ModelSerializer):
    currencyid = CurrencySerializer(source='fk_currencyid', read_only=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_afpid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = Afp
        fields = ('__all__')
        read_only_fields = ['date']

    def create(self, validated_data, instance=None):
        afp = Afp()
        afp.amount = validated_data['amount']
        afp.comment = validated_data['comment']
        afp.fk_currencyid = validated_data['fk_currencyid']
        afp.fk_processid = validated_data['fk_processid']
        afp.date = datetime.now().strftime("%Y-%m-%d")
        afp.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, afp.fk_processid, afp.pk_afpid, profileId)

        return afp


class ApprovalStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalStage
        fields = ('__all__')


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        branch = Branch.objects.create(**validated_data)
        branch.save()
        bid = Branch.objects.latest('pk_branchid')

        return branch


class VendorSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_vendorid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = Vendor
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        vendor = Vendor.objects.create(**validated_data)
        vendor.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, vendor.fk_processid, vendor.pk_vendorid, profileId)
        return vendor


class PayableWaiverSerializer(serializers.ModelSerializer):
    currencyid = CurrencySerializer(source='fk_currencyid', read_only=True)
    vendorid = VendorSerializer(source='fk_vendorid', read_only=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_payable_waiverid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = PayableWaiver
        fields = ('__all__')
        read_only_fields = ['waiver_date']

    def create(self, validated_data, instance=None):
        payable_waiver = PayableWaiver()
        payable_waiver.order_number = validated_data['order_number']
        payable_waiver.order_amount = validated_data['order_amount']
        payable_waiver.invoice_number = validated_data['invoice_number']
        payable_waiver.remarks = validated_data['remarks']
        payable_waiver.fk_currencyid = validated_data['fk_currencyid']
        payable_waiver.fk_processid = validated_data['fk_processid']
        payable_waiver.fk_vendorid = validated_data['fk_vendorid']
        payable_waiver.waiver_date = datetime.now().strftime("%Y-%m-%d")
        payable_waiver.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, payable_waiver.fk_processid, payable_waiver.pk_payable_waiverid, profileId)
        return payable_waiver


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('__all__')


class BranchDepartmentSerializer(serializers.ModelSerializer):
    branchid = BranchSerializer(source='fk_branchid', read_only=True)
    departmentid = DepartmentSerializer(
        source='fk_departmentid', read_only=True)

    class Meta:
        model = BranchDepartment
        fields = ('__all__')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        employee = Employee.objects.create(**validated_data)
        employee.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, employee.fk_processid, employee.pk_employeeid, profileId)

        return employee


class VoucherSerializer(serializers.ModelSerializer):
    # expenseSheet = ExpenseSheetSerializer(
    #     source='fk_expense_sheetid', read_only=True)

    class Meta:
        model = Voucher
        fields = ('__all__')


class ExpenseSheetSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(source="fk_currencyid", read_only=True)
    vouchers = VoucherSerializer(read_only=True, many=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_expense_sheetid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = ExpenseSheet
        fields = ('__all__')
        read_only_fields = ['date']

    def create(self, validated_data, instance=None):

        expenseSheet = ExpenseSheet.objects.create(**validated_data)
        expenseSheet.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, expenseSheet.fk_processid, expenseSheet.pk_expense_sheetid, profileId)

        return expenseSheet


class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialYear
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        financialYear = FinancialYear()
        financialYear.start_date = validated_data.get('start_date')
        financialYear.end_date = validated_data.get('end_date')
        financialYear.status = validated_data.get('status')
        financialYear.save()

        return financialYear


class FuelRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelRequest
        fields = ('__all__')
        read_only_fields = ['date']

    def create(self, validated_data, instance=None):
        fuel = FuelRequest()
        fuel.quantity = validated_data['quantity']
        fuel.comment = validated_data['comment']
        fuel.fk_processid = validated_data['fk_processid']
        fuel.date = datetime.now().strftime("%Y-%m-%d")
        fuel.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, fuel.fk_processid, fuel.pk_fuel_requestid, profileId)

        return fuel


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('__all__')


class ProcessApprovalStageSerializer(serializers.ModelSerializer):
    approval_stage = ApprovalStageSerializer(
        source="fk_approval_stageid", read_only=True)
    process = ProcessSerializer(
        source="fk_processid", read_only=True)
    fk_roleid = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProcessApprovalStage
        fields = ('__all__')

    def create(self, validated_data):
        process_approval_stage = ProcessApprovalStage()
        process_approval_stage.fk_approval_stageid = validated_data['fk_approval_stageid']
        process_approval_stage.fk_processid = validated_data['fk_processid']
        process_approval_stage.approval_stage_number = validated_data['approval_stage_number']
        process_approval_stage.approval_stage_status = validated_data['approval_stage_status']
        process_approval_stage.save()

        SerializerHelper.create_approval_role(
            self, process_approval_stage, validated_data['fk_roleid'])

        return process_approval_stage


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('__all__')


class ProfileFKSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True, source='user')

    class Meta:
        model = Profile
        fields = ('__all__')


class ProfileRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer(source='fk_roleid', read_only=True)
    profile = ProfileFKSerializer(source='fk_profileid', read_only=True)

    class Meta:
        model = ProfileRole
        fields = ('__all__')


class RolePermissionSerializer(serializers.ModelSerializer):
    permission = PermissionSerializer(source="fk_permissionid", read_only=True)
    role = RoleSerializer(source="fk_roleid", read_only=True)

    class Meta:
        model = RolePermission
        fields = ('__all__')


class SystemConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfig
        fields = ('__all__')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True, source='user')

    class Meta:
        model = Profile
        fields = ('__all__')


class HelpTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpTopic
        fields = ('__all__')


class HelpdeskSerializer(serializers.ModelSerializer):
    help_topicid = HelpTopicSerializer(
        source='fk_help_topicid', read_only=True)
    profileid = UserProfileSerializer(source='fk_profileid', read_only=True)

    class Meta:
        model = Helpdesk
        fields = ('__all__')
        read_only_fields = ['fk_profileid', 'created_date']

    def create(self, validated_data, instance=None):
        issue = Helpdesk()
        issue.fk_help_topicid = validated_data['fk_help_topicid']
        issue.fk_profileid = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)
        issue.issue = validated_data['issue']
        issue.created_date = datetime.now().strftime("%Y-%m-%d")
        issue.save()
        user_issue = Helpdesk.objects.latest('pk_helpdeskid')
        helpdesk_admins = ProfileRole.objects.filter(
            fk_roleid__role='Helpdesk')
        DataPointMailer.helpdesk_admin_notification(
            helpdesk_admins, user_issue)
        return issue

    def update(self, instance, validated_data):
        instance.fk_help_topicid = validated_data.get(
            'fk_help_topicid', instance.fk_help_topicid)
        instance.issue = validated_data.get('issue', instance.issue)
        instance.save()
        return instance


class HelpdeskFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = HelpdeskFile
        fields = ('__all__')


class HelpdeskStatusSerializer(serializers.ModelSerializer):
    profileid = UserProfileSerializer(source='fk_profileid', read_only=True)

    class Meta:
        model = IssueStatus
        fields = ('__all__')
        read_only_fields = ['fk_profileid', 'date']

    def create(self, validated_data, instance=None):
        status = IssueStatus()
        status.fk_helpdeskid = validated_data['fk_helpdeskid']
        status.fk_profileid = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)
        status.comment = validated_data['comment']
        status.status = validated_data['status']
        status.date = datetime.now().strftime("%Y-%m-%d")
        status.save()

        issue_status = IssueStatus.objects.latest('pk_issue_statusid')
        helpdesk_admins = ProfileRole.objects.filter(
            fk_roleid__role='Helpdesk')

        DataPointMailer.helpdesk_status_notification(
            helpdesk_admins, issue_status)
        return status


class ProjectsSerializer(serializers.ModelSerializer):
    financial_yearid = FinancialYearSerializer(
        source='fk_financial_yearid', read_only=True)
    currencyid = CurrencySerializer(source='fk_currencyid', read_only=True)
    branch_departmentid = BranchDepartmentSerializer(
        source='fk_branch_departmentid', read_only=True)
    expenditure = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('__all__')

    def get_expenditure(self, obj):
        expenses = GocAmount.objects.filter(
            fk_gocid__fk_projectid=getattr(obj, 'pk'))
        total_expense = 0
        for expense in expenses:
            total_expense = total_expense+expense.goc_amount

        data = {
            'total_expenses': total_expense,
            'balance': getattr(obj, 'budget_amount')-total_expense
        }
        return data


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = ('__all__')


class NewEmployeeSerializer(serializers.ModelSerializer):
    branchid = BranchSerializer(source='fk_branchid', read_only=True)
    departmentid = DepartmentSerializer(
        source='fk_departmentid', read_only=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_new_employeeid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = NewEmployee
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        new_employee = NewEmployee()
        new_employee.fk_processid = validated_data['fk_processid']
        new_employee.fk_branchid = validated_data['fk_branchid']
        new_employee.fk_departmentid = validated_data['fk_departmentid']
        new_employee.firstname = validated_data['firstname']
        new_employee.lastname = validated_data['lastname']
        new_employee.position = validated_data['position']
        new_employee.igg = validated_data['igg']
        new_employee.requirements = validated_data['requirements']
        new_employee.comment = validated_data['comment']
        new_employee.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, new_employee.fk_processid, new_employee.pk_new_employeeid, profileId)

        return new_employee


class StationeryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationeryType
        fields = ('__all__')


class StationeryDetailSerializer(serializers.ModelSerializer):
    stationaryType = StationeryTypeSerializer(
        source='fk_stationery_typeid', read_only=True)
    # stationary = StationerySerializer(source='fk_stationeryid', read_only=True)

    class Meta:
        model = StationeryDetail
        fields = ('__all__')


class StationerySerializer(serializers.ModelSerializer):
    stationary_details = StationeryDetailSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_stationeryid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = Stationery
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        stationery = Stationery.objects.create(**validated_data)
        stationery.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, stationery.fk_processid, stationery.pk_stationeryid, profileId)

        return stationery


class MileageDetailSerializer(serializers.ModelSerializer):
    # mileage = MileageSerializer(source='fk_mileageid', read_only=True)

    class Meta:
        model = MileageDetail
        fields = ('__all__')


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ('__all__')


class MileageSerializer(serializers.ModelSerializer):
    mileageDetails = MileageDetailSerializer(many=True, read_only=True)
    Vehicle = VehicleSerializer(source='fk_vehicleid', read_only=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_mileageid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = Mileage
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        mileage = Mileage.objects.create(**validated_data)
        mileage.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, mileage.fk_processid, mileage.pk_mileageid, profileId)

        return mileage


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ('__all__')


class NatureMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureMovement
        fields = ('__all__')


class AssetSerializer(serializers.ModelSerializer):
    assetType = AssetTypeSerializer(source='fk_asset_typeid', read_only=True)

    class Meta:
        model = Asset
        fields = ('__all__')


class AssetMovementSerializer(serializers.ModelSerializer):
    process = ProcessSerializer(
        source='fk_processid', read_only=True)
    natureMovement = NatureMovementSerializer(
        source='fk_nature_movementid', read_only=True)
    fromStation = StationSerializer(source='fk_from_stationid', read_only=True)
    toStation = StationSerializer(source='fk_to_stationid', read_only=True)
    assets = AssetSerializer(many=True, read_only=True)

    class Meta:
        model = AssetMovement
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        assetMovement = AssetMovement.objects.create(**validated_data)
        assetMovement.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, assetMovement.fk_processid, assetMovement.pk_asset_movementid, profileId)

        return assetMovement


class OvertimeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OvertimeDetail
        fields = ('__all__')


class SapRightsSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_sap_rightid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = SapRights
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        saprights = SapRights.objects.create(**validated_data)
        saprights.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, saprights.fk_processid, saprights.pk_sap_rightid, profileId)

        return saprights


class EquipmentSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_equipmentid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = Equipment
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        equipment = Equipment.objects.create(**validated_data)
        equipment.save()
        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, equipment.fk_processid, equipment.pk_equipmentid, profileId)

        return equipment


class OvertimeSerializer(serializers.ModelSerializer):
    overtimeDetails = OvertimeDetailSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_overtimeid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = Overtime
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        overtime = Overtime.objects.create(**validated_data)
        overtime.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, overtime.fk_processid, overtime.pk_overtimeid, profileId)

        return overtime


class AssetDisposalSerializer(serializers.ModelSerializer):
    assetType = AssetTypeSerializer(source="fk_asset_typeid", read_only=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_asset_disposalid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = AssetDisposal
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        assetDisposal = AssetDisposal.objects.create(**validated_data)
        assetDisposal.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, assetDisposal.fk_processid, assetDisposal.pk_asset_disposalid, profileId)

        return assetDisposal


class OvertimeDetailSerializer(serializers.ModelSerializer):
    overtime = OvertimeSerializer(source='fk_overtimeid', read_only=True)

    class Meta:
        model = OvertimeDetail
        fields = ('__all__')


class WorkFlowRightsSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_workflow_rightid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = WorkflowRights
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        workflow_rights = WorkflowRights.objects.create(**validated_data)
        workflow_rights.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, workflow_rights.fk_processid, workflow_rights.pk_workflow_rightid, profileId)

        return workflow_rights


class AllowanceAttSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowanceAtt
        fields = ('__all__')
        read_only_fields = ['fk_travelid']


class FuelAttSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelAtt
        fields = ('__all__')
        read_only_fields = ['fk_travelid']


class TravelSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')
    allowance_att = serializers.SerializerMethodField(
        'get_allowance')
    fuel_att = serializers.SerializerMethodField(
        'get_fuel')
    allowanceAtt = AllowanceAttSerializer(required=False)
    fuelAtt = FuelAttSerializer(required=False)

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_travelid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    def get_allowance(self, obj):
        if obj.allowance:
            try:
                allowanceAtt = AllowanceAtt.objects.get(
                    fk_travelid=obj.pk_travelid)
                allowanceAmount = allowanceAtt.allowanceAmount
                allowanceReason = allowanceAtt.allowanceReason
            except AllowanceAtt.DoesNotExist:
                allowanceAmount = None
                allowanceReason = None
            data = {'allowanceAmount': allowanceAmount,
                    'allowanceReason': allowanceReason}
            return data

    def get_fuel(self, obj):
        if obj.fuel_requirement:
            try:
                fuelAtt = FuelAtt.objects.get(fk_travelid=obj.pk_travelid)
                fuelAmount = fuelAtt.fuelAmount
                fuelReason = fuelAtt.fuelReason
                vehicle = fuelAtt.vehicle
                fuelType = fuelAtt.fuelType
                distance = fuelAtt.distance
                local_running = fuelAtt.local_running
                unit_cost = fuelAtt.unit_cost
                total_cost = fuelAtt.total_cost
            except FuelAtt.DoesNotExist:
                fuelAmount = None
                fuelReason = None
                vehicle = None
                fuelType = None
                distance = None
                local_running = None
                unit_cost = None
                total_cost = None
            data = {
                'fuelAmount': fuelAmount,
                'fuelReason': fuelReason,
                'vehicle': vehicle,
                'fuelType': fuelType,
                'distance': distance,
                'local_running': local_running,
                'unit_cost': unit_cost,
                'total_cost': total_cost
            }
            return data

    class Meta:
        model = Travel
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        travel = Travel()
        travel.route = validated_data['route']
        travel.destination = validated_data['destination']
        travel.period_from = validated_data['period_from']
        travel.period_to = validated_data['period_to']
        travel.purpose = validated_data['purpose']
        travel.fuel_requirement = validated_data['fuel_requirement']
        travel.allowance = validated_data['allowance']
        travel.accomodation = validated_data['accomodation']
        travel.mode = validated_data['mode']
        travel.category = validated_data['category']
        travel.fk_processid = validated_data['fk_processid']
        travel.save()

        if validated_data['fuel_requirement']:
            fuel_data = validated_data.pop('fuelAtt')
            fuel_att = FuelAtt.objects.update_or_create(
                fk_travelid=travel, **fuel_data)

        if validated_data['allowance']:
            allowance_data = validated_data.pop('allowanceAtt')
            AllowanceAtt.objects.update_or_create(
                fk_travelid=travel, **allowance_data)

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, travel.fk_processid, travel.pk_travelid, profileId)

        return travel

    def update(self, instance, validated_data):
        instance.route = validated_data['route']
        instance.destination = validated_data['destination']
        instance.period_from = validated_data['period_from']
        instance.period_to = validated_data['period_to']
        instance.purpose = validated_data['purpose']
        instance.fuel_requirement = validated_data['fuel_requirement']
        instance.allowance = validated_data['allowance']
        instance.accomodation = validated_data['accomodation']
        instance.mode = validated_data['mode']
        instance.category = validated_data['category']
        instance.fk_processid = validated_data['fk_processid']
        instance.save()

        if validated_data['fuel_requirement']:
            fuel_data = validated_data.pop('fuelAtt')
            try:
                fuel_att = FuelAtt.objects.get(fk_travelid=instance)
                fuel_att.fuelAmount = fuel_data['fuelAmount']
                fuel_att.fuelReason = fuel_data['fuelReason']
                fuel_att.vehicle = fuel_data['vehicle']
                fuel_att.fuelType = fuel_data['fuelType']
                fuel_att.distance = fuel_data['distance']
                fuel_att.local_running = fuel_data['local_running']
                fuel_att.unit_cost = fuel_data['unit_cost']
                fuel_att.total_cost = fuel_data['total_cost']
                fuel_att.save()
            except FuelAtt.DoesNotExist:
                FuelAtt(fk_travelid=instance, **fuel_data).save()

        if validated_data['allowance']:
            allowance_data = validated_data.pop('allowanceAtt')
            try:
                allowance_att = AllowanceAtt.objects.get(
                    fk_travelid=instance)
                allowance_att.allowanceAmount = allowance_data['allowanceAmount']
                allowance_att.allowanceReason = allowance_data['allowanceReason']
                allowance_att.save()
            except AllowanceAtt.DoesNotExist:
                AllowanceAtt(fk_travelid=instance, **allowance_data).save()
        return instance


class ApprovalRoleSerializer(serializers.ModelSerializer):
    process_approval_stage = ProcessApprovalStageSerializer(
        source="fk_process_approval_stageid", read_only=True)
    role = RoleSerializer(source="fk_roleid", read_only=True)

    class Meta:
        model = ApprovalRole
        fields = ('__all__')


class FileSerializer(serializers.ModelSerializer):
    # request = RequestSerializer(source='fk_requestid', read_only=True)

    class Meta:
        model = File
        fields = ('__all__')
        read_only_fields = ['date']


class RequestSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    profile = ProfileFKSerializer(source="fk_profileid", read_only=True)
    process = ProcessSerializer(source="fk_processid", read_only=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            approval = Approval.objects.get(
                fk_requestid=obj.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = Request
        fields = ('__all__')
        read_only_fields = ['date']


class GOCAmountSerializer(serializers.ModelSerializer):

    class Meta:
        model = GocAmount
        fields = ('__all__')
        read_only_fields = ['date']


class GocSerializer(serializers.ModelSerializer):
    gocAmounts = GOCAmountSerializer(many=True, read_only=True)
    # project = ProjectsSerializer(many=True, read_only=True)
    expenditure = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_gocid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = Goc
        fields = ('__all__')
        read_only_fields = ['date']

    def get_or_none(self, pk):
        try:
            expenses = GocAmount.objects.get(fk_gocid=pk)
            return 100
        except GocAmount.DoesNotExist:
            return 'Data Not Found'

    def get_expenditure(self, obj):
        goc = Goc.objects.get(pk=getattr(obj, 'pk'))
        budget_amount = Project.objects.get(
            pk=goc.fk_projectid.pk).budget_amount
        expenses = GocAmount.objects.filter(
            fk_gocid__fk_projectid=goc.fk_projectid, fk_gocid__lte=goc.pk)
        total_expense = 0
        for expense in expenses:
            total_expense = total_expense+expense.goc_amount

        data = {
            'total_expenses': total_expense,
            'balance': budget_amount - total_expense
        }
        return data

    def create(self, validated_data, instance=None):
        goc = Goc()
        goc.comment = validated_data['comment']
        goc.fk_processid = validated_data['fk_processid']
        goc.fk_projectid = validated_data['fk_projectid']
        goc.date = datetime.now().strftime("%Y-%m-%d")
        goc.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, goc.fk_processid, goc.pk_gocid, profileId)
        return goc


class ProcessStageApproverSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source="fk_profileid", read_only=True)
    approval_role = ApprovalRoleSerializer(
        source="fk_approval_roleid", read_only=True)

    class Meta:
        model = ProcessStageApprover
        fields = ('__all__')


class ApprovalSerializer(serializers.ModelSerializer):
    process_id = serializers.IntegerField(write_only=True)
    approval_stages = serializers.JSONField(write_only=True)
    process_stage_approvers = serializers.JSONField(write_only=True)
    isDenied = serializers.BooleanField(write_only=True)

    class Meta:
        model = Approval
        fields = ('__all__')
        read_only_fields = ['fk_financial_yearid',
                            'fk_process_stage_approverid', 'fk_process_approval_stageid', 'status', 'process_id', 'isDenied']

    def create(self, validated_data):
        # validated_data = data.testData()
        approval = Approval()
        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)
        financial_year = SerializerHelper.get_current_financial_year(self)

        SerializerHelper.approve_request(
            self, validated_data, profileId, financial_year)
        return approval


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('__all__')


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('password')

    def update(self, instance, validated_data):
        password = SerializerHelper.random_password(self)
        if validated_data['password']:
            password = validated_data['password']
        instance.password = make_password(password)
        instance.save()
        DataPointMailer.password_reset(instance, password)
        return instance


class SystemBackUpSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='fk_profileid', read_only=True)

    class Meta:
        model = SystemBackup
        fields = ('__all__')
        read_only_fields = ['date', 'backup_file', 'fk_profileid']

    def create(self, validated_data, instance=None):
        output = sp.getoutput('python manage.py dbbackup')
        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)
        systemBackup = SystemBackup()

        systemBackup.backup_file = output.split('to')[1]
        systemBackup.fk_profileid = profileId
        systemBackup.save()

        return systemBackup


class ManualJournalRequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualJournalRequestDetail
        fields = ('__all__')


class ManualJournalRequestSerializer(serializers.ModelSerializer):
    details = ManualJournalRequestDetailSerializer(
        many=True, read_only=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_manual_journal_requestid, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = ManualJournalRequest
        fields = ('__all__')
        read_only_fields = ['posting_date']

    def create(self, validated_data, instance=None):
        manualJournalRequest = ManualJournalRequest()
        manualJournalRequest.accrual = validated_data['accrual']
        manualJournalRequest.currency = validated_data['currency']
        manualJournalRequest.date = validated_data['date']
        manualJournalRequest.doc_type = validated_data['doc_type']
        manualJournalRequest.fk_processid = validated_data['fk_processid']
        manualJournalRequest.for_reversal_next_period = validated_data['for_reversal_next_period']
        manualJournalRequest.forex_rate = validated_data['forex_rate']
        manualJournalRequest.header_text = validated_data['header_text']
        manualJournalRequest.provision = validated_data['provision']
        manualJournalRequest.recurring = validated_data['recurring']
        manualJournalRequest.reference = validated_data['reference']
        manualJournalRequest.currency = validated_data['currency']
        manualJournalRequest.currency = validated_data['currency']
        manualJournalRequest.company_code = validated_data['company_code']

        manualJournalRequest.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, manualJournalRequest.fk_processid, manualJournalRequest.pk_manual_journal_requestid, profileId)
        return manualJournalRequest


class ProfileDepartmentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(source='fk_departmentid', read_only=True)
    profile = ProfileFKSerializer(source='fk_profileid', read_only=True)

    class Meta:
        model = ProfileDepartment
        fields = ('__all__')


class HandoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Handover
        fields = ('__all__')

class CardLoadItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardItem
        fields = ('__all__')        

class CardAccountLoadingSerializer(serializers.ModelSerializer):
    # card_items = CardLoadItemsSerializer(read_only=True, many=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_cal_id, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = Cal
        fields = ('__all__')

    def create(self, validated_data, instance=None):

        cal = Cal.objects.create(**validated_data)
        cal.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, cal.fk_processid, cal.pk_cal_id, profileId)

        return cal       


class CardCreateItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardCreateItem
        fields = ('__all__')        

class CardCreateSerializer(serializers.ModelSerializer):
    # cao_items = CardCreateItemsSerializer(read_only=True, many=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_cao_id, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = Cao
        fields = ('__all__')

    def create(self, validated_data, instance=None):

        cao = Cao.objects.create(**validated_data)
        cao.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, cao.fk_processid, cao.pk_cao_id, profileId)

        return cao    


class CacLubricantSerializer(serializers.ModelSerializer):

    class Meta:
        model = CacLubricant
        fields = ('__all__')  


class CacProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CacProduct
        fields = ('__all__')  


class CacSerializer(serializers.ModelSerializer):
    # cac_lubricants = CacLubricantSerializer(read_only=True, many=True)
    # cac_products = CacProductSerializer(read_only=True, many=True)
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        try:
            request = Request.objects.get(
                workflow_id=obj.pk_cac_id, fk_processid=obj.fk_processid_id)
            approval = Approval.objects.get(
                fk_requestid=request.pk_requestid, status=1)
            data = {'approval_status': approval.approval_status,
                    'approval_stage': approval.fk_process_approval_stageid.fk_approval_stageid.approval_stage}
        except Approval.DoesNotExist:
            data = {'approval_status': "Not Submited", 'approval_stage': None}
        return data

    class Meta:
        model = Cac
        fields = ('__all__')

    def create(self, validated_data, instance=None):
        cac = Cac.objects.create(**validated_data)
        cac.save()

        profileId = SerializerHelper.get_profile_id(
            self, self.context['request'].user.id)

        SerializerHelper.create_request(
            self, cac.fk_processid, cac.pk_cac_id, profileId)

        return cac    
