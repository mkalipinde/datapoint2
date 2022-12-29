import re
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from .models import *
from datetime import datetime
from rest_framework import serializers
import json
from .email_service import DataPointMailer


class ViewsHelper:

    def get_profile(self, queryset, user_id):
        if user_id != None:
            user_data = queryset.filter(user__id=user_id)[:1]
            if user_data.exists():
                return user_data
            else:
                raise APIException("User data not found!")
        else:
            return queryset

    def get_profile_id(request):
        user_id = request.user.id
        return Profile.objects.filter(user=user_id)[0]

    def instance(request_id, instance_object):
        return instance_object.objects.filter(user=user_id)[0]

    def get_helpdesk_status(self, queryset, helpdesk_id):
        if helpdesk_id != None:
            helpdesk_status = queryset.filter(fk_helpdeskid=helpdesk_id)
            if len(helpdesk_status) != 0:
                return helpdesk_status
            else:
                return []
        else:
            return queryset

    def get_config(self, queryset):
        config = queryset
        if len(config) != 0:
            return config
        else:
            return queryset

    def get_process_category(self, queryset, process_categoryid):
        process_category = queryset.filter(
            fk_process_categoryid=process_categoryid)
        if len(process_category) != 0:
            return process_category
        else:
            return []

    def filter_by_process_code(self, queryset, process_code):

        process = queryset.filter(
            process_code=process_code)
        if len(process) != 0:
            return process
        else:
            return queryset

    def get_afps(self, queryset):
        DataPointMailer.test_mailer(self)
        return queryset

    def get_permissions(self, queryset, roleId, profileid):
        raise APIException(profileid)

    def filter_stationery(self, queryset, fkStationeryId):
        if fkStationeryId != None:
            return queryset.filter(fk_stationeryid=fkStationeryId)
        return queryset

    def filter_Mileage(self, queryset, fkmileageId):
        if fkmileageId != None:
            return queryset.filter(fk_mileageid=fkmileageId)
        return queryset

    def filter_mileage_vehicle(self, queryset, fkvehicleid):
        if fkvehicleid != None:
            return queryset.filter(fk_vehicleid=fkvehicleid)
        return queryset

    def filter_overtime(self, queryset, fkovertimeId):
        if fkovertimeId != None:
            return queryset.filter(fk_overtimeid=fkovertimeId)
        return queryset

    def filter_voucher(self, queryset, expenseSheetId):
        if expenseSheetId != None:
            return queryset.filter(fk_expense_sheetid=expenseSheetId)
        return queryset

    def create_workflow(self, request):
        process_approval_stage = ProcessApprovalStage()
        process_approval_stage.fk_processid = self.request.data.get(
            'fk_processid')
        process_approval_stage.fk_approval_stageid = self.request.data.get(
            'fk_approval_stageid')
        process_approval_stage.save()
        return process_approval_stage

    def get_process_approval_stages(self, queryset, processid):
        if processid != None:
            return queryset.filter(fk_processid=processid, approval_stage_status='Active').order_by('approval_stage_number')
        else:
            return queryset

    def get_process_next_approval_stage(self, currect_stage_number, processid):
        try:
            return ProcessApprovalStage.objects.get(
                fk_processid=processid, approval_stage_number=currect_stage_number+1,  approval_stage_status='Active')
        except:
            ProcessApprovalStage.DoesNotExist
            return False

    def get_process_current_approval_stage(self, currect_stage_number, processid):
        try:
            return ProcessApprovalStage.objects.get(fk_processid=processid, approval_stage_number=currect_stage_number, approval_stage_status='Active')
        except:
            ProcessApprovalStage.DoesNotExist
            return False

    def get_process_stage_approver(process_approval_stageid, stage_number, profile, request_profile):
        approval_role = ApprovalRole.objects.get(
            fk_process_approval_stageid=process_approval_stageid)

        if stage_number == 0:
            try:
                process_stage_approver = ProcessStageApprover.objects.get(
                    fk_approval_roleid=approval_role.pk_approval_roleid, fk_profileid=profile, approver_status='active')
            except:
                ProcessStageApprover.DoesNotExist
                stage_approver = ProcessStageApprover()
                stage_approver.fk_profileid = profile
                stage_approver.fk_approval_roleid = approval_role
                stage_approver.approver_status = "Active"
                stage_approver.approver_level = 1
                stage_approver.save()
                process_stage_approver = ProcessStageApprover.objects.get(
                    pk_process_stage_approverid=stage_approver.pk)
            return process_stage_approver

        if approval_role.fk_roleid.role == 'HOD':
            user_department = ProfileDepartment.objects.filter(
                fk_profileid=request_profile).order_by(
                'fk_departmentid').first()

            hod = Role.objects.get(role='HOD')

            hod_profile_roles = ProfileRole.objects.filter(
                fk_roleid=hod.pk_roleid)

            for hod_profile_role in hod_profile_roles:
                hod_profile = ProfileDepartment.objects.filter(
                    fk_departmentid=user_department.fk_departmentid, fk_profileid=hod_profile_role.fk_profileid).order_by(
                    'fk_departmentid').first()
                try:
                    process_stage_approver = ProcessStageApprover.objects.get(
                        fk_approval_roleid=approval_role.pk_approval_roleid, fk_profileid=hod_profile.fk_profileid, approver_status='active')
                    return process_stage_approver
                except:
                    ProcessStageApprover.DoesNotExist
            raise APIException('HOD not available')
        try:
            process_stage_approver = ProcessStageApprover.objects.filter(
                fk_approval_roleid=approval_role.pk_approval_roleid, fk_profileid=profile, approver_status='active', ).order_by('approver_level').first()
            return process_stage_approver
        except:
            ProcessStageApprover.DoesNotExist
            raise APIException('User not permitted to approve request')

# ----------------------
    def get_current_process_stage_approvers(process_approval_stageid, request_profile):
        approval_role = ApprovalRole.objects.get(
            fk_process_approval_stageid=process_approval_stageid)

        if approval_role.fk_roleid.role == 'HOD':
            user_department = ProfileDepartment.objects.filter(
                fk_profileid=request_profile).order_by(
                'fk_departmentid').first()

            department_users = ProfileDepartment.objects.filter(
                fk_departmentid=user_department.fk_departmentid)

            for department_user in department_users:
                try:
                    hod_profile = ProfileRole.objects.get(
                        fk_roleid__role='HOD', fk_profileid=department_user.fk_profileid)
                    try:
                        process_stage_approver = ProcessStageApprover.objects.get(
                            fk_approval_roleid=approval_role.pk_approval_roleid, fk_profileid=hod_profile.fk_profileid, approver_status='Active')
                        if process_stage_approver:
                            process_stage_approver = process_stage_approver = ProcessStageApprover.objects.filter(
                                fk_approval_roleid=approval_role.pk_approval_roleid, fk_profileid=process_stage_approver.fk_profileid, approver_status='Active')
                            return process_stage_approver
                    except:
                        print('Not found')
                        ProcessStageApprover.DoesNotExist

                except:
                    ProfileRole.DoesNotExist

                # print(department_user.fk_profileid)
                # hod = Role.objects.get(role='HOD')

                # hod_profile_roles = ProfileRole.objects.filter(
                #     fk_roleid=hod.pk_roleid)

                # for hod_profile_role in hod_profile_roles:
                #     hod_profile = ProfileDepartment.objects.filter(
                #         fk_departmentid=user_department.fk_departmentid, fk_profileid=hod_profile_role.fk_profileid).order_by(
                #         'fk_departmentid').first()

                #     process_stage_approvers = ProcessStageApprover.objects.filter(
                #         fk_approval_roleid=approval_role.pk_approval_roleid, approver_status='Active')

                #     for process_stage_approver in process_stage_approvers:
                #         user = ProfileDepartment.objects.get(
                #             fk_profileid=process_stage_approver.fk_profileid)

                #         if user:
                #             print(user.fk_profileid)
                #         # if process_stage_approver:
                #         #     return process_stage_approver

            raise APIException('HOD not available')

        try:
            process_stage_approvers = ProcessStageApprover.objects.filter(
                fk_approval_roleid=approval_role.pk_approval_roleid, approver_status='active',)
            return process_stage_approvers
        except:
            ProcessStageApprover.DoesNotExist
            raise APIException('User not permitted to approve request')
# ----------------------

    def delete_process_approval_stage(self, queryset, delete_stage):
        if delete_stage != None:
            queryset.filter(pk_process_approval_stageid=delete_stage).update(
                approval_stage_status='Inactive')
        return queryset

    def get_approval_stage_role(self, queryset, stageid):
        if stageid != None:
            return queryset.filter(fk_process_approval_stageid=stageid)
        else:
            return queryset

    def get_profile_roles(self, queryset, profile_id, role_id):
        if profile_id != None:
            return queryset.filter(fk_profileid=profile_id)
        elif role_id != None:
            return queryset.filter(fk_roleid__pk_roleid=role_id)
        else:
            return queryset

    def get_request_workflowid_process(self, queryset, processId, workflowId):
        if processId != None and workflowId != None:
            return queryset.filter(fk_processid=processId).filter(workflow_id=workflowId)
        else:
            return queryset

    def get_process_approval_roles(self, queryset, process_id, status):
        if process_id != None:
            return queryset.filter(fk_process_approval_stageid__fk_processid=process_id, fk_process_approval_stageid__approval_stage_status=status).order_by('fk_process_approval_stageid__approval_stage_number')
        else:
            return queryset

    def get_process_stage_approvers(self, queryset, process_id):
        if process_id != None:
            return queryset.filter(fk_approval_roleid__fk_process_approval_stageid__fk_processid=process_id, approver_status='Active').order_by('approver_level')
        else:
            return queryset

    def get_approval(self, queryset, request_id):
        if request_id != None:
            return queryset.filter(fk_requestid=request_id)
        else:
            return queryset

    def get_active_notifications(self, queryset, profile_id):
        if profile_id != None:
            return queryset.filter(profile_id=profile_id)
        else:
            return queryset

    def get_profile_role_permissions(self, queryset, profile_id, permission_code):
        if profile_id and permission_code != None:
            profile_roles = ProfileRole.objects.filter(fk_profileid=profile_id)
            for profile_role in profile_roles:
                profile_role_permission = queryset.filter(
                    fk_permissionid__permission_code=permission_code, fk_roleid__pk_roleid=profile_role.fk_roleid.pk_roleid)
                if len(profile_role_permission) != 0:
                    return profile_role_permission
            return {}
        else:
            return {}

    def get_branch_departments(self, queryset, branch_id, department_id):
        if branch_id != None:
            return queryset.filter(fk_branchid=branch_id)
        elif department_id != None:
            return queryset.filter(fk_departmentid=department_id)
        else:
            return queryset

    def get_branch_departments(self, queryset, branch_id, department_id):
        if branch_id != None:
            return queryset.filter(fk_branchid=branch_id)
        elif department_id != None:
            return queryset.filter(fk_departmentid=department_id)
        else:
            return queryset

    def get_profile_departments(self, queryset, profile_id, department_id):
        if profile_id != None:
            return queryset.filter(fk_profileid=profile_id)
        elif department_id != None:
            return queryset.filter(fk_departmentid=department_id)
        else:
            return queryset

    def get_user_requests(self, queryset):
        return queryset

    def approve_request(request, financial_year,
                        process_stage_approver, process_approval_stage, comment):

        Approval.objects.filter(
            fk_requestid_id=request, status=1).update(status=0)

        approval = Approval()
        approval.fk_requestid_id = request
        approval.fk_financial_yearid = financial_year
        approval.fk_process_stage_approverid_id = process_stage_approver
        approval.fk_process_approval_stageid_id = process_approval_stage
        approval.comment = comment
        approval.status = 1
        approval.save()
        return approval

    def reject_request(request, financial_year,
                       process_stage_approver, process_approval_stage, comment):

        Approval.objects.filter(
            fk_requestid_id=request, status=1).update(status=0)

        approval = Approval()
        approval.fk_requestid_id = request
        approval.fk_financial_yearid = financial_year
        approval.fk_process_stage_approverid_id = process_stage_approver
        approval.fk_process_approval_stageid_id = process_approval_stage
        approval.comment = comment
        approval.status = 0
        approval.approval_status = 'RE'
        approval.save()
        return approval

    def approved_request(request):
        approval = Approval.objects.filter(
            fk_requestid_id=request, status=1).update(approval_status='AP')
        return approval

    # def reject_request(request):
    #     approval = Approval.objects.filter(
    #         fk_requestid_id=request, status=1).update(approval_status='RE')
    #     return approval
