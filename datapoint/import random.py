import random
import datetime
from datetime import timedelta
from re import A
import re
from django.http.response import HttpResponse

from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.exceptions import APIException
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
        requestid = validated_data.get('fk_requestid').pk_requestid

        approval_stages = ViewsHelper.get_process_approval_stages(
            self, ProcessApprovalStage.objects.all(), process_id)

        request = Request.objects.get(
            pk_requestid=requestid)

        approval_data = Approval.objects.filter(
            fk_requestid=requestid)

        if not approval_stages.exists():
            raise APIException('Approval workflow not set')

        if approval_data.exists():
            approvaldata = Approval.objects.filter(
                fk_requestid=requestid, status=1).order_by('-pk_approvalid').first()

            request_stage = ViewsHelper.get_process_next_approval_stage(
                self, approvaldata.fk_process_approval_stageid.approval_stage_number, process_id)

            process_stage_approver = ViewsHelper.get_process_stage_approver(
                request_stage.pk_process_approval_stageid, approvaldata.fk_process_approval_stageid.approval_stage_number, profileId)

            process_stage_approver_id = process_stage_approver.pk_process_stage_approverid

            approve_request = ViewsHelper.approve_request(requestid, financial_year,
                                                          process_stage_approver_id, request_stage.pk_process_approval_stageid)

            request_next_stage = ViewsHelper.get_process_next_approval_stage(
                self, request_stage.approval_stage_number, process_id)

            process_stage_approver = ViewsHelper.get_process_stage_approver(
                request_stage.pk_process_approval_stageid, request_next_stage.approval_stage_number, request.fk_profileid)

            raise APIException(process_stage_approver_id)

            DataPointMailer.add_request_notification(
                self, request, process_stage_approver)

            return approve_request

        if request.fk_profileid == profileId:
            iniate_request_stage = ViewsHelper.get_process_next_approval_stage(
                self, 0, process_id)

            process_stage_approver = ViewsHelper.get_process_stage_approver(
                iniate_request_stage.pk_process_approval_stageid, 0, profileId)

            process_stage_approver_id = process_stage_approver.pk_process_stage_approverid

            approve_request = ViewsHelper.approve_request(requestid, financial_year,
                                                          process_stage_approver_id, iniate_request_stage.pk_process_approval_stageid)

            request_next_stage = ViewsHelper.get_process_next_approval_stage(
                self, iniate_request_stage.approval_stage_number, process_id)

            process_stage_approver = ViewsHelper.get_process_stage_approver(
                iniate_request_stage.pk_process_approval_stageid, request_next_stage.approval_stage_number, request.fk_profileid)

            DataPointMailer.add_request_notification(
                self, request, process_stage_approver)

            return approve_request

        # # This is some bad ass shit
        # request_profile = Request.objects.get(
        #     pk_requestid=validated_data.get('fk_requestid').pk_requestid).fk_profileid
        # workflow_id = validated_data.get('fk_requestid').workflow_id

        # approval_stages = ViewsHelper.get_process_approval_stages(
        #     self, ProcessApprovalStage.objects.all(), validated_data.get('process_id'))
        # approval_stage_array = []
        # for process_stage in approval_stages:
        #     approval_stage_array.append(
        #         process_stage.pk_process_approval_stageid)

        # approval = Approval()
        # approval_stages = validated_data['approval_stages']
        # process_stage_approvers = validated_data['process_stage_approvers']

        # next_approval_stage = ''

        # for approval_stage in approval_stages:
        #     for process_stage_approver in process_stage_approvers:
        #         if (approval_stage['pk_approval_roleid'] == process_stage_approver['approval_role']['pk_approval_roleid']):
        #             if not approval_value:
        #                 if (profileId.pk_profileid == process_stage_approver['profile']['pk_profileid']) and (approval_stage_array[0] == approval_stage['fk_process_approval_stageid']):
        #                     if (approval_stage_array[approval_stage_array.index(approval_stage['process_approval_stage']['pk_process_approval_stageid'])+1]):
        #                         next_approval_stage = approval_stage_array[approval_stage_array.index(
        #                             approval_stage['process_approval_stage']['pk_process_approval_stageid'])+1]
        #                     approval.fk_requestid = validated_data.get(
        #                         'fk_requestid')
        #                     approval.fk_process_stage_approverid = ProcessStageApprover.objects.get(
        #                         pk_process_stage_approverid=process_stage_approver['pk_process_stage_approverid'])
        #                     approval.fk_financial_yearid = financial_year
        #                     approval.fk_process_approval_stageid = ProcessApprovalStage.objects.get(
        #                         pk_process_approval_stageid=approval_stage['fk_process_approval_stageid'])
        #                     approval.status = 1
        #                     approval.save()
        #                     DataPointMailer.add_request_notification(
        #                         self, request_profile, process_stage_approvers, next_approval_stage, workflow_id)
        #                     return approval
        #             else:
        #                 current_approval = Approval.objects.get(
        #                     fk_requestid=validated_data.get('fk_requestid'), status=1)
        #                 if (approval_stage_array.index(current_approval.fk_process_approval_stageid.pk_process_approval_stageid)+1 <= len(approval_stage_array)):
        #                     if (profileId.pk_profileid == process_stage_approver['profile']['pk_profileid']) and (approval_stage_array[approval_stage_array.index(current_approval.fk_process_approval_stageid.pk_process_approval_stageid)+1] == approval_stage['fk_process_approval_stageid']):
        #                         try:
        #                             if (approval_stage_array[approval_stage_array.index(approval_stage['process_approval_stage']['pk_process_approval_stageid'])+1]):
        #                                 next_approval_stage = approval_stage_array[approval_stage_array.index(
        #                                     approval_stage['process_approval_stage']['pk_process_approval_stageid'])+1]
        #                         except IndexError:
        #                             next_approval_stage = ''
        #                         Approval.objects.filter(fk_requestid=validated_data.get(
        #                             'fk_requestid'), status=1).update(status=0)
        #                         approval.fk_requestid = validated_data.get(
        #                             'fk_requestid')
        #                         approval.fk_process_stage_approverid = ProcessStageApprover.objects.get(
        #                             pk_process_stage_approverid=process_stage_approver['pk_process_stage_approverid'])
        #                         approval.fk_financial_yearid = financial_year
        #                         approval.fk_process_approval_stageid = ProcessApprovalStage.objects.get(
        #                             pk_process_approval_stageid=approval_stage['fk_process_approval_stageid'])
        #                         approval.status = 1
        #                         approval.save()
        #                         DataPointMailer.add_request_notification(
        #                             self, request_profile, process_stage_approvers, next_approval_stage, workflow_id)
        #                         return approval
        #                 else:
        #                     return approval
        # return True

    def get_profile_departments(self, departmentid, profile):
        return ProfileDepartment.objects.get(fk_roleid=departmentid, fk_profileid=profile)
