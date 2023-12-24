# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from jsonfield import JSONField


class ApiLog(models.Model):
    pk_api_logid = models.AutoField(primary_key=True)
    fk_profileid = models.ForeignKey(
        'Profile', models.DO_NOTHING, db_column='fk_profileid')
    name = models.CharField(max_length=100)
    action = models.CharField(max_length=45)

    class Meta:

        db_table = 'api_log'


class Approval(models.Model):
    CHOICES = (
        ('PE', 'Pending'),
        ('RE', 'Rejected'),
        ('AP', 'Approved'),
    )
    pk_approvalid = models.AutoField(primary_key=True)
    fk_requestid = models.ForeignKey(
        'Request', models.DO_NOTHING, db_column='fk_requestid')
    fk_financial_yearid = models.ForeignKey(
        'FinancialYear', models.DO_NOTHING, db_column='fk_financial_yearid')
    fk_process_stage_approverid = models.ForeignKey(
        'ProcessStageApprover', models.DO_NOTHING, db_column='fk_process_stage_approverid')
    fk_process_approval_stageid = models.ForeignKey(
        'ProcessApprovalStage', models.DO_NOTHING, db_column='fk_process_approval_stageid')
    status = models.IntegerField()
    comment = models.TextField()
    approval_status = models.CharField(
        max_length=20, choices=CHOICES, default='PE')

    class Meta:

        db_table = 'approval'


class ApprovalRole(models.Model):
    pk_approval_roleid = models.AutoField(primary_key=True)
    fk_process_approval_stageid = models.ForeignKey(
        'ProcessApprovalStage', models.DO_NOTHING, db_column='fk_process_approval_stageid')
    fk_roleid = models.ForeignKey(
        'Role', models.DO_NOTHING, db_column='fk_roleid')

    class Meta:

        db_table = 'approval_role'


class ApprovalStage(models.Model):
    pk_approval_stageid = models.AutoField(primary_key=True)
    approval_stage = models.CharField(max_length=45)
    approval_code = models.CharField(max_length=45)

    class Meta:

        db_table = 'approval_stage'


class Asset(models.Model):
    pk_assetid = models.AutoField(primary_key=True)
    asset = models.CharField(max_length=45)
    fk_asset_typeid = models.ForeignKey(
        'AssetType', models.DO_NOTHING, db_column='fk_asset_typeid')
    fk_asset_movementid = models.ForeignKey(
        'AssetMovement', models.DO_NOTHING, related_name="assets", db_column='fk_asset_movementid')

    class Meta:

        db_table = 'asset'


class AssetDisposal(models.Model):
    pk_asset_disposalid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        'Process', models.DO_NOTHING, db_column='fk_processid')
    fk_asset_typeid = models.ForeignKey(
        'AssetType', models.DO_NOTHING, db_column='fk_asset_typeid')
    comment = models.TextField()
    date = models.DateField()

    class Meta:

        db_table = 'asset_disposal'


class AssetMovement(models.Model):
    pk_asset_movementid = models.AutoField(primary_key=True)
    comment = models.TextField()
    fk_processid = models.ForeignKey(
        'Process', models.DO_NOTHING, db_column='fk_processid')
    fk_nature_movementid = models.ForeignKey(
        'NatureMovement', models.DO_NOTHING, db_column='fk_nature_movementid')
    fk_from_stationid = models.ForeignKey(
        'Station', models.DO_NOTHING, db_column='fk_from_stationid')
    fk_to_stationid = models.ForeignKey(
        'Station', models.DO_NOTHING, db_column='fk_to_stationid', related_name='toStations')
    date = models.DateField()
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'asset_movement'


class AssetType(models.Model):
    pk_asset_typeid = models.AutoField(primary_key=True)
    asset_type = models.CharField(max_length=45)

    class Meta:

        db_table = 'asset_type'


class Branch(models.Model):
    pk_branchid = models.AutoField(primary_key=True)
    branch = models.CharField(max_length=45)

    class Meta:

        db_table = 'branch'


class BranchDepartment(models.Model):
    pk_branch_departmentid = models.AutoField(primary_key=True)
    fk_branchid = models.ForeignKey(
        Branch, models.DO_NOTHING, db_column='fk_branchid')
    fk_departmentid = models.ForeignKey(
        'Department', models.DO_NOTHING, db_column='fk_departmentid')

    class Meta:

        db_table = 'branch_department'


class Currency(models.Model):
    pk_currencyid = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=45)
    code = models.CharField(max_length=45)

    class Meta:

        db_table = 'currency'


class Department(models.Model):
    pk_departmentid = models.AutoField(primary_key=True)
    department = models.CharField(max_length=45)

    class Meta:

        db_table = 'department'


class Employee(models.Model):
    pk_employeeid = models.AutoField(primary_key=True)
    fk_profileid = models.ForeignKey(
        'Profile', models.DO_NOTHING, db_column='fk_profileid')
    fk_branch_departmentid = models.ForeignKey(
        BranchDepartment, models.DO_NOTHING, db_column='fk_branch_departmentid')
    employee_number = models.CharField(max_length=45)

    class Meta:

        db_table = 'employee'


class ExpenseSheet(models.Model):
    pk_expense_sheetid = models.AutoField(primary_key=True)
    fk_currencyid = models.ForeignKey(
        Currency, models.DO_NOTHING, db_column='fk_currencyid')
    amount = models.DecimalField(max_digits=13, decimal_places=5)
    fk_processid = models.ForeignKey(
        'Process', models.DO_NOTHING, db_column='fk_processid')
    # Field renamed because it was a Python reserved word.
    from_field = models.DateField(db_column='from')
    to = models.DateField()
    date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'expense_sheet'


class FinancialYear(models.Model):
    pk_financial_yearid = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.IntegerField()

    class Meta:

        db_table = 'financial_year'


class FuelRequest(models.Model):
    pk_fuel_requestid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        'Process', models.DO_NOTHING, db_column='fk_processid')
    quantity = models.DecimalField(max_digits=13, decimal_places=5)
    comment = models.TextField()
    date = models.DateTimeField()

    class Meta:

        db_table = 'fuel_request'


class Goc(models.Model):
    pk_gocid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        'Process', models.DO_NOTHING, db_column='fk_processid')
    fk_projectid = models.ForeignKey(
        'Project', models.DO_NOTHING, db_column='fk_projectid')
    comment = models.TextField()
    date = models.DateField()
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'goc'


class GocAmount(models.Model):
    pk_goc_amountid = models.AutoField(primary_key=True)
    fk_gocid = models.ForeignKey(
        Goc, models.DO_NOTHING, db_column='fk_gocid', related_name='gocAmounts')
    goc_amount = models.DecimalField(
        max_digits=20, decimal_places=2)

    class Meta:

        db_table = 'goc_amount'


class HelpTopic(models.Model):
    pk_help_topicid = models.AutoField(primary_key=True)
    help_topic = models.CharField(max_length=45)
    description = models.CharField(max_length=45)

    class Meta:

        db_table = 'help_topic'


class Helpdesk(models.Model):
    pk_helpdeskid = models.AutoField(primary_key=True)
    fk_help_topicid = models.ForeignKey(
        HelpTopic, models.DO_NOTHING, db_column='fk_help_topicid')
    fk_profileid = models.ForeignKey(
        'Profile', models.DO_NOTHING, db_column='fk_profileid')
    issue = models.TextField()
    created_date = models.DateField()

    class Meta:

        db_table = 'helpdesk'


class IssueStatus(models.Model):
    pk_issue_statusid = models.AutoField(primary_key=True)
    fk_helpdeskid = models.ForeignKey(
        Helpdesk, models.DO_NOTHING, db_column='fk_helpdeskid')
    fk_profileid = models.ForeignKey(
        'Profile', models.DO_NOTHING, db_column='fk_profileid')
    comment = models.TextField()
    date = models.DateField()
    status = models.IntegerField()

    class Meta:

        db_table = 'issue_status'


class NatureMovement(models.Model):
    pk_nature_movementid = models.AutoField(primary_key=True)
    nature_movement = models.CharField(max_length=45)

    class Meta:

        db_table = 'nature_movement'


class PayableWaiver(models.Model):
    pk_payable_waiverid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        'Process', models.DO_NOTHING, db_column='fk_processid')
    fk_vendorid = models.ForeignKey(
        'Vendor', models.DO_NOTHING, db_column='fk_vendorid')
    order_number = models.CharField(max_length=45)
    order_amount = models.DecimalField(max_digits=20, decimal_places=3)
    fk_currencyid = models.ForeignKey(
        Currency, models.DO_NOTHING, db_column='fk_currencyid')
    invoice_number = models.CharField(max_length=45)
    remarks = models.TextField()
    waiver_date = models.DateField()
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'payable_waiver'


class Permission(models.Model):
    pk_permissionid = models.AutoField(primary_key=True)
    permission = models.CharField(max_length=45)
    permission_code = models.CharField(max_length=45)
    description = models.TextField()

    class Meta:

        db_table = 'permission'


class Process(models.Model):
    pk_processid = models.AutoField(primary_key=True)
    fk_process_categoryid = models.ForeignKey(
        'ProcessCategory', models.DO_NOTHING, db_column='fk_process_categoryid')
    process = models.TextField()
    process_code = models.CharField(max_length=45)
    status = models.BooleanField(max_length=1, default=1)

    class Meta:

        db_table = 'process'


class ProcessApprovalStage(models.Model):
    pk_process_approval_stageid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        Process, models.DO_NOTHING, db_column='fk_processid')
    fk_approval_stageid = models.ForeignKey(
        ApprovalStage, models.DO_NOTHING, db_column='fk_approval_stageid')
    approval_stage_number = models.IntegerField()
    approval_stage_status = models.CharField(max_length=8)

    class Meta:

        db_table = 'process_approval_stage'


class ProcessCategory(models.Model):
    pk_process_categoryid = models.AutoField(primary_key=True)
    process_category = models.CharField(max_length=45)

    class Meta:

        db_table = 'process_category'


class ProcessStageApprover(models.Model):
    pk_process_stage_approverid = models.AutoField(primary_key=True)
    fk_profileid = models.ForeignKey(
        'Profile', models.DO_NOTHING, db_column='fk_profileid')
    fk_approval_roleid = models.ForeignKey(
        ApprovalRole, models.DO_NOTHING, db_column='fk_approval_roleid')
    approver_status = models.CharField(max_length=8)
    approver_level = models.IntegerField()

    class Meta:

        db_table = 'process_stage_approver'


class Profile(models.Model):
    pk_profileid = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    mobile = models.CharField(max_length=20)
    profile_img = models.CharField(max_length=45)
    status = models.BooleanField(max_length=1)

    class Meta:

        db_table = 'profile'


class ProfileRole(models.Model):
    pk_profile_roleid = models.AutoField(primary_key=True)
    fk_profileid = models.ForeignKey(
        Profile, models.DO_NOTHING, db_column='fk_profileid')
    fk_roleid = models.ForeignKey(
        'Role', models.DO_NOTHING, db_column='fk_roleid')

    class Meta:

        db_table = 'profile_role'


class Project(models.Model):
    pk_projectid = models.AutoField(primary_key=True)
    fk_branch_departmentid = models.ForeignKey(
        BranchDepartment, models.DO_NOTHING, db_column='fk_branch_departmentid')
    fk_financial_yearid = models.ForeignKey(
        FinancialYear, models.DO_NOTHING, db_column='fk_financial_yearid')
    fk_currencyid = models.ForeignKey(
        Currency, models.DO_NOTHING, db_column='fk_currencyid')
    project = models.CharField(max_length=45)
    description = models.TextField()
    budget_amount = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.BooleanField(default=True)

    class Meta:

        db_table = 'project'


class Role(models.Model):
    pk_roleid = models.AutoField(primary_key=True)
    role = models.TextField()
    description = models.TextField()

    class Meta:

        db_table = 'role'


class RolePermission(models.Model):
    pk_role_permissionid = models.AutoField(primary_key=True)
    fk_roleid = models.ForeignKey(
        Role, models.DO_NOTHING, db_column='fk_roleid')
    fk_permissionid = models.ForeignKey(
        Permission, models.DO_NOTHING, db_column='fk_permissionid')

    class Meta:
        unique_together = [('fk_roleid', 'fk_permissionid')]
        db_table = 'role_permission'


class Station(models.Model):
    pk_stationid = models.AutoField(primary_key=True)
    station = models.CharField(max_length=45)

    class Meta:

        db_table = 'station'


class SystemConfig(models.Model):
    pk_system_configid = models.AutoField(primary_key=True)
    time_out = models.CharField(max_length=45)
    backup_time = models.CharField(max_length=45)
    backup_frequency = models.CharField(max_length=45)

    class Meta:

        db_table = 'system_config'


class Vendor(models.Model):
    pk_vendorid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        Process, models.DO_NOTHING, db_column='fk_processid')
    vendor = models.CharField(max_length=200)
    business_type = models.TextField(blank=True, null=True)
    physical_address = models.TextField(blank=True, null=True)
    postal_address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=45)
    email = models.CharField(max_length=80)
    searchTerm = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    fax = models.TextField(blank=True, null=True)
    wh_tax_country = models.TextField(blank=True, null=True)
    wh_tax_type = models.TextField(blank=True, null=True)
    wh_tax_code = models.TextField(blank=True, null=True)
    payment_term = models.TextField(blank=True, null=True)
    payment_method = models.TextField(blank=True, null=True)
    trading_partner = models.TextField(blank=True, null=True)
    tax_number = models.TextField(blank=True, null=True)
    acc_group = models.TextField(blank=True, null=True)
    reconciliation_acc = models.TextField(blank=True, null=True)

    # Bank details
    bank_name = models.TextField(blank=True, null=True)
    bank_country = models.TextField(blank=True, null=True)
    bank_address = models.TextField(blank=True, null=True)
    bank_branch = models.TextField(blank=True, null=True)
    acc_name = models.TextField(blank=True, null=True)
    bank_key = models.TextField(blank=True, null=True)
    swift = models.TextField(blank=True, null=True)
    acc_num = models.TextField(blank=True, null=True)
    instruction_key = models.TextField(blank=True, null=True)
    acc_key = models.TextField(blank=True, null=True)
    partner_category = models.TextField(blank=True, null=True)
    bank_contact_person = models.TextField(blank=True, null=True)
    bank_contact_email = models.TextField(blank=True, null=True)
    iban = models.TextField(blank=True, null=True)
    # contact_persons
    contact_person_1 = models.TextField(blank=True, null=True)
    contact_person_1_designation = models.TextField(blank=True, null=True)
    contact_person_1_email = models.TextField(blank=True, null=True)
    contact_person_1_phone = models.TextField(blank=True, null=True)
    contact_person_2 = models.TextField(blank=True, null=True)
    contact_person_2_designation = models.TextField(blank=True, null=True)
    contact_person_2_email = models.TextField(blank=True, null=True)
    contact_person_2_phone = models.TextField(blank=True, null=True)
    # purchasingData
    organisation = models.TextField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True)
    incoterm = models.TextField(blank=True, null=True)
    sales_person = models.TextField(blank=True, null=True)
    contact_number = models.TextField(blank=True, null=True)
    service_desc = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=1)

    class Meta:
        db_table = 'vendor'


class Voucher(models.Model):
    pk_voucherid = models.AutoField(primary_key=True)
    fk_expense_sheetid = models.ForeignKey(
        ExpenseSheet, models.DO_NOTHING, db_column='fk_expense_sheetid', related_name="vouchers")
    voucher_number = models.CharField(max_length=45)
    amount = models.DecimalField(max_digits=13, decimal_places=5)
    expense_incurred = models.TextField()
    date = models.DateField()

    class Meta:

        db_table = 'voucher'


class Afp(models.Model):
    pk_afpid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        'Process', models.DO_NOTHING, db_column='fk_processid')
    fk_currencyid = models.ForeignKey(
        Currency, models.DO_NOTHING, db_column='fk_currencyid')
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    comment = models.TextField()
    date = models.DateTimeField()
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'afp'


class Equipment(models.Model):
    pk_equipmentid = models.AutoField(primary_key=True)
    equipment = models.CharField(max_length=45)
    date_from = models.DateField()
    date_to = models.DateField()
    reason = models.TextField()
    fk_processid = models.ForeignKey(
        'Process', models.DO_NOTHING, db_column='fk_processid')

    class Meta:

        db_table = 'equipment'


class Travel(models.Model):
    pk_travelid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        Process, models.DO_NOTHING, db_column='fk_processid')
    route = models.CharField(max_length=45)
    destination = models.CharField(max_length=45)
    period_from = models.DateField()
    period_to = models.CharField(max_length=45)
    purpose = models.TextField()
    fuel_requirement = models.IntegerField()
    allowance = models.IntegerField()
    accomodation = models.IntegerField()
    mode = models.CharField(max_length=45)
    category = models.CharField(max_length=45)
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'travel'


class Fuel(models.Model):
    pk_fuelid = models.AutoField(primary_key=True)
    fk_travelid = models.ForeignKey(
        'Travel', models.DO_NOTHING, db_column='fk_travelid')
    reg_number = models.CharField(max_length=45)
    fuel_type = models.IntegerField()
    distance = models.DecimalField(max_digits=13, decimal_places=3)
    distance_local = models.DecimalField(max_digits=13, decimal_places=3)
    quantity = models.DecimalField(max_digits=13, decimal_places=3)
    cost = models.DecimalField(max_digits=13, decimal_places=3)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    return_time = models.TimeField()
    return_arrival = models.TimeField()

    class Meta:

        db_table = 'fuel'


class FuelAtt(models.Model):
    pk_fuel_attid = models.AutoField(primary_key=True)
    fk_travelid = models.ForeignKey(
        'Travel', models.DO_NOTHING, db_column='fk_travelid')
    fuelAmount = models.DecimalField(max_digits=13, decimal_places=2)
    fuelReason = models.TextField()
    vehicle = models.TextField()
    fuelType = models.TextField()
    distance = models.TextField()
    local_running = models.TextField()
    unit_cost = models.TextField()
    total_cost = models.TextField()

    class Meta:
        db_table = 'fuel_att'


class AllowanceAtt(models.Model):
    pk_allowance_attid = models.AutoField(primary_key=True)
    fk_travelid = models.ForeignKey(
        'Travel', models.DO_NOTHING, db_column='fk_travelid')
    allowanceAmount = models.DecimalField(max_digits=13, decimal_places=2)
    allowanceReason = models.TextField()

    class Meta:
        db_table = 'allowance_att'


class Requirements(models.Model):
    pk_requirementid = models.IntegerField(primary_key=True)
    fk_travelid = models.ForeignKey(
        'Travel', models.DO_NOTHING, db_column='fk_travelid')
    fk_currencyid = models.ForeignKey(
        Currency, models.DO_NOTHING, db_column='fk_currencyid')
    requirement = models.CharField(max_length=45)
    amount = models.DecimalField(max_digits=13, decimal_places=3)
    comment = models.TextField()

    class Meta:

        db_table = 'requirements'


class Mileage(models.Model):
    pk_mileageid = models.AutoField(primary_key=True)
    fk_vehicleid = models.ForeignKey(
        'Vehicle', models.DO_NOTHING, db_column='fk_vehicleid', related_name='mileages'
    )
    fk_processid = models.ForeignKey(
        'Process', models.DO_NOTHING, db_column='fk_processid')

    class Meta:

        db_table = 'mileage'


class MileageDetail(models.Model):
    pk_mileage_detailid = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    start_km = models.IntegerField()
    end_km = models.IntegerField()
    company_km = models.IntegerField()
    home_office = models.IntegerField()
    own_km = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    fk_mileageid = models.ForeignKey(
        Mileage, models.DO_NOTHING, db_column='fk_mileageid', related_name="mileageDetails")

    class Meta:

        db_table = 'mileage_detail'


class Overtime(models.Model):
    pk_overtimeid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        'Process', models.DO_NOTHING, db_column='fk_processid')
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'overtime'


class OvertimeDetail(models.Model):
    pk_overtime_detailid = models.AutoField(primary_key=True)
    description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_category = models.IntegerField()
    date = models.DateField()
    fk_overtimeid = models.ForeignKey(
        Overtime, models.DO_NOTHING, related_name='overtimeDetails', db_column='fk_overtimeid')

    class Meta:

        db_table = 'overtime_detail'


class SapRights(models.Model):
    pk_sap_rightid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        Process, models.DO_NOTHING, db_column='fk_processid')
    sap_rights = models.TextField()
    description = models.TextField()
    date_from = models.DateField()
    date_to = models.DateField()
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'sap_rights'


class Stationery(models.Model):
    pk_stationeryid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        Process, models.DO_NOTHING, db_column='fk_processid')
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'stationery'


class StationeryType(models.Model):
    pk_stationery_typeid = models.AutoField(primary_key=True)
    type = models.CharField(max_length=45)

    class Meta:

        db_table = 'stationery_type'


class StationeryDetail(models.Model):
    pk_stationery_detailid = models.AutoField(primary_key=True)
    fk_stationeryid = models.ForeignKey(
        Stationery, models.DO_NOTHING, db_column='fk_stationeryid', related_name='stationary_details')
    fk_stationery_typeid = models.ForeignKey(
        'StationeryType', models.DO_NOTHING, db_column='fk_stationery_typeid')
    quantity = models.IntegerField()

    class Meta:

        db_table = 'stationery_detail'


class WorkflowRights(models.Model):
    pk_workflow_rightid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        Process, models.DO_NOTHING, db_column='fk_processid')
    description = models.TextField()
    date_from = models.DateField()
    date_to = models.DateField()
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'workflow_rights'


class NewEmployee(models.Model):
    pk_new_employeeid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        Process, models.DO_NOTHING, db_column='fk_processid')
    fk_branchid = models.ForeignKey(
        Branch, models.DO_NOTHING, db_column='fk_branchid')
    fk_departmentid = models.ForeignKey(
        Department, models.DO_NOTHING, db_column='fk_departmentid')
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    position = models.CharField(max_length=45)
    igg = models.CharField(max_length=45)
    requirements = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'new_employee'


class Request(models.Model):
    pk_requestid = models.AutoField(primary_key=True)
    workflow_id = models.IntegerField()
    fk_processid = models.ForeignKey(
        'Process', models.DO_NOTHING, db_column='fk_processid')
    fk_profileid = models.ForeignKey(
        'Profile', models.DO_NOTHING, db_column='fk_profileid')
    date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=1)

    class Meta:
        unique_together = [('workflow_id', 'fk_processid')]
        db_table = 'request'


class File(models.Model):
    pk_fileid = models.AutoField(primary_key=True)
    fk_requestid = models.ForeignKey(
        'Request', models.DO_NOTHING, db_column='fk_requestid', related_name="files")
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    name = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)

    class Meta:

        db_table = 'file'


class Notification(models.Model):
    pk_notificationid = models.AutoField(primary_key=True)
    fk_requestid = models.ForeignKey(
        'Request', models.DO_NOTHING, db_column='fk_requestid')
    name = models.CharField(max_length=45)
    profile_id = models.IntegerField()
    workflow = models.IntegerField()
    process = models.CharField(max_length=45)
    process_code = models.CharField(max_length=45)
    requested_by = models.CharField(max_length=45)
    url = models.CharField(max_length=100)
    date_created = models.DateField()
    status = models.IntegerField()

    class Meta:
        db_table = 'notification'


class SystemBackup(models.Model):
    pk_system_backup = models.AutoField(primary_key=True)
    backup_file = models.TextField()
    fk_profileid = models.ForeignKey(
        'Profile', models.DO_NOTHING, db_column='fk_profileid')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'system_backup'


class ManualJournalRequest(models.Model):
    pk_manual_journal_requestid = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(
        Process, models.DO_NOTHING, db_column='fk_processid')
    date = models.DateField()
    doc_type = models.TextField()
    currency = models.TextField(max_length=4)
    forex_rate = models.TextField(max_length=10)
    reference = models.TextField(max_length=100)
    header_text = models.TextField()
    for_reversal_next_period = models.BooleanField()
    recurring = models.BooleanField()
    accrual = models.BooleanField()
    provision = models.BooleanField()
    posting_date = models.DateTimeField(default=timezone.now)
    company_code = models.TextField()
    status = models.BooleanField(default=1)

    class Meta:
        db_table = 'manual_journal_request'


class ManualJournalRequestDetail(models.Model):
    pk_manual_request_detailid = models.AutoField(primary_key=True)
    posting_key = models.TextField(max_length=100)
    fk_manual_journal_requestid = models.ForeignKey(
        ManualJournalRequest, models.DO_NOTHING, db_column='fk_manual_journal_requestid', related_name="details")
    account = models.TextField(max_length=100)
    gl_indicator = models.TextField(max_length=100)
    account_description = models.TextField()
    amount_in_doc_currency = models.TextField(max_length=100)
    amount_in_local_currency = models.TextField(max_length=50)
    tax_code = models.TextField(max_length=100)
    material = models.TextField()
    assignment = models.TextField()
    text = models.TextField()
    cost_center = models.TextField(max_length=50)
    internal_order = models.TextField(max_length=500)

    class Meta:
        db_table = 'manual_journal_request_detail'


class Vehicle(models.Model):
    pk_vehicleid = models.AutoField(primary_key=True)
    vehicle = models.CharField(max_length=45)
    reg = models.CharField(max_length=45)
    mileage = models.CharField(max_length=45)
    fuel = models.CharField(max_length=45)
    year = models.DateField()

    class Meta:
        db_table = 'vehicle'


class ProfileDepartment(models.Model):
    pk_profile_departmentid = models.AutoField(primary_key=True)
    fk_profileid = models.ForeignKey(
        Profile, models.DO_NOTHING, db_column='fk_profileid')
    fk_departmentid = models.ForeignKey(
        'Department', models.DO_NOTHING, db_column='fk_departmentid')

    class Meta:
        db_table = 'profile_department'


class HelpdeskFile(models.Model):
    pk_helpdesk_fileid = models.AutoField(primary_key=True)
    fk_helpdeskid = models.ForeignKey(
        'Helpdesk', models.DO_NOTHING, db_column='fk_helpdeskid')
    file = models.FileField(upload_to='documents/helpdesk/%Y/%m/%d/')
    date = models.DateTimeField(default=timezone.now)

    class Meta:

        db_table = 'helpdesk_file'


class Handover(models.Model):
    pk_handoverid = models.AutoField(primary_key=True)
    my_profileid = models.IntegerField()
    to_profileid = models.ForeignKey(
        'Profile', models.DO_NOTHING, db_column='to_profileid')
    date_from = models.DateField()
    date_to = models.DateField()
    status = models.BooleanField(default=1)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'handover'

class Cal(models.Model):
    pk_cal_id = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(Process, models.DO_NOTHING, db_column='fk_processid')
    client_name = models.TextField(blank=True, null=True)
    account = models.CharField(max_length=45)
    cards = JSONField()
    date = models.DateField()
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'cal'


class CardItem(models.Model):
    pk_card_id = models.AutoField(primary_key=True)
    fk_cal_id = models.ForeignKey(Cal, models.DO_NOTHING, db_column='fk_cal_id', related_name="card_items")
    card_number = models.CharField(max_length=45)
    card_name = models.TextField(blank=True, null=True)
    pin = models.IntegerField()
    management_code = models.TextField(blank=True, null=True)
    geographical_zone = models.TextField(blank=True, null=True)
    litres = models.IntegerField()
    override_possibility = models.TextField(blank=True, null=True)
    amount_credited = models.IntegerField()
    cal = models.TextField(blank=True, null=True)
    date = models.DateField()
    
    class Meta:

        db_table = 'card_item'   



class Cao(models.Model):
    pk_cao_id = models.AutoField(primary_key=True)
    fk_processid = models.ForeignKey(Process, models.DO_NOTHING, db_column='fk_processid')
    company_name = models.TextField(blank=True, null=True)
    applicant_name = models.CharField(max_length=200)
    applicant_designation = models.CharField(max_length=100)
    applicant_phone = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    card_type = models.TextField(blank=True, null=True)
    request_type = models.CharField(max_length=100)
    cards = JSONField()
    date = models.DateField()
    status = models.BooleanField(default=1)

    class Meta:

        db_table = 'cao'


class CardCreateItem(models.Model):
    pk_card_id = models.AutoField(primary_key=True)
    fk_cao_id = models.ForeignKey(Cao, models.DO_NOTHING, db_column='fk_cao_id', related_name="cao_items")
    card_name = models.TextField(blank=True, null=True)
    reg_number = models.CharField(max_length=45)
    prod_service = models.CharField(max_length=45)
    value = models.IntegerField()
    mileage_check = models.CharField(max_length=100)
    tank_cap = models.IntegerField()
    tank_cap_override = models.CharField(max_length=100)
    pin = models.IntegerField()
    management_code = models.TextField(blank=True, null=True)
    auth_days = models.CharField(max_length=100)
    auth_hrs = models.CharField(max_length=100)
    period_override = models.CharField(max_length=100)
    geographical_zone = models.TextField(blank=True, null=True)
    override_geo = models.CharField(max_length=100)
    monthly_volume_limit = models.IntegerField()
    override_volume = models.CharField(max_length=100)
    monthly_credit_limit = models.IntegerField()
    override_credit = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'card_create_item'    


class Cac(models.Model):
    pk_cac_id=models.AutoField(primary_key=True)
    fk_processid=models.ForeignKey(Process, models.DO_NOTHING, db_column='fk_processid')
    date=models.CharField(max_length=100)
    request_type=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    contract_ref=models.CharField(max_length=100)
    channel=models.CharField(max_length=100)
    sub_channel=models.CharField(max_length=100)
    supply_ref=models.CharField(max_length=100)
    area_n_salesman=models.CharField(max_length=100)
    ownership=models.CharField(max_length=100)
    litre_rate=models.IntegerField()
    service_charge=models.CharField(max_length=100)
    discount=models.CharField(max_length=100)
    fin_charges=models.CharField(max_length=100)
    security_deposit=models.CharField(max_length=100)
    rent=models.CharField(max_length=100)
    capacities=models.CharField(max_length=100)
    credit_limit=models.CharField(max_length=100)
    bank_guarantee=models.CharField(max_length=100)
    payment_mode=models.CharField(max_length=100)
    tax_status=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)
    other=models.CharField(max_length=100)
    cus_address=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    contact_name=models.CharField(max_length=100)
    contact_email=models.CharField(max_length=100)
    delivery_address=models.CharField(max_length=100)
    delivery_phone=models.CharField(max_length=100)
    delivery_contact_name=models.CharField(max_length=100)
    delivery_telex=models.CharField(max_length=100)
    distance_from_depot=models.CharField(max_length=100)
    dr_kg_rate=models.CharField(max_length=100)
    dr_from=models.CharField(max_length=100)
    rebate_rate=models.CharField(max_length=100)
    rebate_ceiling=models.CharField(max_length=100)
    cd_ac=models.CharField(max_length=100)
    cd_look_up_code=models.CharField(max_length=100)
    cd_bf_bal=models.CharField(max_length=100)
    cd_third_party=models.CharField(max_length=100)
    cd_channel=models.CharField(max_length=100)
    cd_sales=models.CharField(max_length=100)
    cd_dormant=models.CharField(max_length=100)
    cd_fin_charges=models.CharField(max_length=100)
    cd_access_group=models.CharField(max_length=100)
    cd_comments=models.CharField(max_length=100)
    cd_pin_code=models.CharField(max_length=100)
    cd_crd_limit=models.CharField(max_length=100)
    cd_payment_terms=models.CharField(max_length=100)
    cd_cus_address_code=models.CharField(max_length=100)
    cd_cus_fiscal_st=models.CharField(max_length=100)
    cd_cus_crd_cntrl=models.CharField(max_length=100)
    cd_cus_comments=models.CharField(max_length=100)
    cd_dv_address_code=models.CharField(max_length=100)
    cd_dv_dist=models.CharField(max_length=100)
    cd_dv_fiscal_st=models.CharField(max_length=100)
    cd_dv_crd_ctrl=models.CharField(max_length=100)
    cd_dv_comments=models.CharField(max_length=100)  
    status = models.BooleanField(default=1)

    class Meta:
        db_table = 'cac'    

class CacLubricant(models.Model):  
    pk_lubricant_id=models.AutoField(primary_key=True)
    fk_cac_id = models.ForeignKey(Cac, models.DO_NOTHING, db_column='fk_cac_id', related_name="cac_lubricants")
    lubricant_number=models.IntegerField()
    currency=models.CharField(max_length=100)
    product=models.CharField(max_length=100)
    desc=models.TextField()
    unit_price=models.IntegerField()
    litres=models.IntegerField()
    cac_from=models.CharField(max_length=100)
    to=models.CharField(max_length=100)

    class Meta:
        db_table = 'cac_lubricant'  



class CacProduct(models.Model):  
    pk_product_id=models.AutoField(primary_key=True)
    fk_cac_id = models.ForeignKey(Cac, models.DO_NOTHING, db_column='fk_cac_id', related_name="cac_products")
    product_name=models.CharField(max_length=100)
    litre_rate=models.IntegerField()
    litre_from=models.CharField(max_length=100)
    unit_rate=models.IntegerField()
    unit_from=models.CharField(max_length=100)
    cyl_bulk=models.CharField(max_length=100)

    class Meta:
        db_table = 'cac_product'                         

class ProjectRequest(models.Model):
    id=models.AutoField(primary_key=True)
    fk_processid=models.ForeignKey(Process, models.DO_NOTHING, db_column='fk_processid')
    title=models.TextField()
    phone=models.TextField()
    start_date=models.DateField()
    complete_date=models.DateField()
    project_type=models.TextField()
    budget=models.TextField()
    location =models.TextField()
    sponsor= models.TextField()
    manager = models.TextField()
    summary= models.TextField()
    objectives = models.TextField()
    justification= models.TextField()
    case_fast_track= models.TextField()
    dependencies = models.TextField()
    tech= models.TextField()
    risk=models.TextField()
    in_scope=models.TextField()
    out_scope=models.TextField()
    cost_overview=models.TextField()
    grand_total=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
      db_table = 'project_request'



class ProjectStakeholder(models.Model):
    id=models.AutoField(primary_key=True)
    project_request_id=models.ForeignKey(ProjectRequest, models.DO_NOTHING, db_column='project_request_id', related_name="stakeholders")
    name=models.TextField()
    role=models.TextField()
    contact_info=models.TextField()
    class Meta:
      db_table = 'project_stakeholder'

class ProjectMilestone(models.Model):
    id=models.AutoField(primary_key=True)
    project_request_id=models.ForeignKey(ProjectRequest, models.DO_NOTHING, db_column='project_request_id', related_name="milestones")
    name=models.TextField()
    deadline= models.DateField()
    class Meta:
      db_table = 'project_milestone'

class ProjectStaffRes(models.Model):
    id=models.AutoField(primary_key=True)
    project_request_id=models.ForeignKey(ProjectRequest, models.DO_NOTHING, db_column='project_request_id', related_name="staff_resources")
    function=models.TextField()
    capability= models.TextField()
    fte= models.TextField()
    class Meta:
      db_table = 'project_staff_resource'
