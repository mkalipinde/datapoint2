import random
import datetime
from datetime import timedelta
from re import A
from django.http.response import HttpResponse

from rest_framework import HTTP_HEADER_ENCODING
from .models import *
from .views_helper import ViewsHelper
from .email_service import *


class SerializerHelper:
    def random_password(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pw_length = 10
        mypw = ""

        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            mypw = mypw + alphabet[next_index]
        return mypw

    def add_default_role(self, username):
        profile_id = Profile.objects.filter(
            user__username=username).values_list('pk_profileid')[0][0]
        profile_role = ProfileRole(fk_profileid_id=profile_id, fk_roleidid=2)
        profile_role.save()
        return profile_role

    def api_log(self, name, action):
        log_data = ApiLog(name=name, action=action)
        log_data.save()
        api_log = ApiLog.objects.latest()
        return api_log

    def get_profile_id(self, user_id):
        return Profile.objects.get(user=user_id)

    def workflow(self, data):
        print(data)
        process_approval_stage = ProcessApprovalStage(fk_processid=self.data['fk_processid'], fk_approval_stageid=[
                                                      'fk_approval_stageid'], approval_stage_status=1)
        process_approval_stage.save()
        return process_approval_stage

    def create_request(self, processId, workflowId, profile):
        request = Request()
        request.fk_profileid = profile
        request.fk_processid = processId
        request.workflow_id = workflowId
        request.save()
        return request

    def get_process_approval_stage(self, process_approval_stageid):
        return ApprovalRole.objects.filter(fk_process_approval_stageid=process_approval_stageid)

    def get_profile_role(self, roleid, profile):
        return ProfileRole.objects.get(fk_roleid=roleid, fk_profileid=profile)

    def create_approval_role(self, processApprovalStage, roleid):
        role = Role.objects.filter(pk_roleid=roleid)[0]
        approval_role = ApprovalRole()
        approval_role.fk_process_approval_stageid = processApprovalStage
        approval_role.fk_roleid = role
        approval_role.save()
        return approval_role

    def get_current_financial_year(self):
        return FinancialYear.objects.get(status=1)

    def approve_request(self, validated_data, profileId, financial_year):
        process_id = validated_data.get('process_id')
        comment = validated_data.get('comment')
        request_id = validated_data.get('fk_requestid').pk_requestid
        

        approval_stages = ViewsHelper.get_process_approval_stages(
            self, ProcessApprovalStage.objects.all(), process_id)
    

        request = Request.objects.get(
            pk_requestid=request_id)

        approval_data = Approval.objects.filter(
            fk_requestid=request_id)

        if not approval_stages.exists():
            raise APIException('Approval workflow not set')

        if approval_data.exists():
            approvaldata = Approval.objects.filter(
                fk_requestid=request_id).order_by('-pk_approvalid').first()

            if approvaldata.approval_status == 'RE':
                raise APIException(
                    'Attempting to approve a rejected request is not allowed')

            approvaldata = Approval.objects.filter(
                fk_requestid=request_id, status=1).order_by('-pk_approvalid').first()

            current_request_stage = ViewsHelper.get_process_current_approval_stage(
                self, approvaldata.fk_process_approval_stageid.approval_stage_number, process_id)

            next_request_stage = ViewsHelper.get_process_next_approval_stage(
                self, current_request_stage.approval_stage_number, process_id)

            process_stage_approver = ViewsHelper.get_process_stage_approver(
                next_request_stage.pk_process_approval_stageid, next_request_stage.approval_stage_number, profileId, request.fk_profileid)
            

            process_stage_approver_id = process_stage_approver.pk_process_stage_approverid



            if validated_data.get('isDenied'):
                reject_request = ViewsHelper.reject_request(request_id, financial_year,
                                                            process_stage_approver_id, next_request_stage.pk_process_approval_stageid, comment)
                DataPointMailer.reject_request_notification_email(
                    self, request)
                return reject_request

            approve_request = ViewsHelper.approve_request(request_id, financial_year,
                                                          process_stage_approver_id, next_request_stage.pk_process_approval_stageid, comment)

            approvaldata = Approval.objects.filter(
                fk_requestid=request_id, status=1).order_by('-pk_approvalid').first()

            current_request_stage = ViewsHelper.get_process_current_approval_stage(
                self, approvaldata.fk_process_approval_stageid.approval_stage_number, process_id)

            next_request_stage = ViewsHelper.get_process_next_approval_stage(
                self, current_request_stage.approval_stage_number, process_id)

            if not next_request_stage:
                approve_request = ViewsHelper.approved_request(request_id)
                DataPointMailer.approved_request_notification_email(
                    self, request)
                return approve_request

            process_stage_approvers = ViewsHelper.get_current_process_stage_approvers(
                next_request_stage.pk_process_approval_stageid, request.fk_profileid)
            
         

            DataPointMailer.request_notification_email(
                self, request, process_stage_approvers)
            return approve_request

        if request.fk_profileid == profileId:
            iniate_request_stage = ViewsHelper.get_process_next_approval_stage(
                self, 0, process_id)

            process_stage_approver = ViewsHelper.get_process_stage_approver(
                iniate_request_stage.pk_process_approval_stageid, 0, profileId, request.fk_profileid)

            process_stage_approver_id = process_stage_approver.pk_process_stage_approverid

            approve_request = ViewsHelper.approve_request(request_id, financial_year,
                                                          process_stage_approver_id, iniate_request_stage.pk_process_approval_stageid, comment)

            request_next_stage = ViewsHelper.get_process_next_approval_stage(
                self, iniate_request_stage.approval_stage_number, process_id)

            process_stage_approvers = ViewsHelper.get_current_process_stage_approvers(
                request_next_stage.pk_process_approval_stageid, request.fk_profileid)

            DataPointMailer.request_notification_email(
                self, request, process_stage_approvers)
            return approve_request

        raise APIException('User not permitted to initiate request')

    def get_profile_departments(self, departmentid, profile):
        return ProfileDepartment.objects.get(fk_roleid=departmentid, fk_profileid=profile)
