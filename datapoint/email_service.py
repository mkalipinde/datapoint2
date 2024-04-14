import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import AsyncIterable

from rest_framework.exceptions import APIException
from .url_helper import *
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template


class DataPointMailer():
    def test_mailer(self):
        server = smtplib.SMTP('smtp.mailtrap.io', 2525)
        server.starttls()
        server.login("cf3ea4dcbfb9e1", "cf1582f2649d11")

        # Send the mail
        message = """From: NoReply <noreply@totalmalawisystems.com>
To: Joel <jkumwenda@gmail.com>
Subject: Datapoint Workflow

        Is there any new crouse planned?
        """
        usern = 'jkumwenda@gmail.com@inbox.mailtrap.io'
        server.sendmail(usern, usern, message)

    def add_user(self, username, password, email, name):
        with open(settings.BASE_DIR+"/templates/request_approval_email.txt") as txt_message:
            user_registration_message = txt_message.read()+" Username: " + \
                username+" Email: "+email
        email_message = EmailMultiAlternatives(
            'DRF Base API Account', user_registration_message, 'no-reply@example.com', to=[email])
        html_template = get_template("new_user_email.html").render(
            {'name': name, 'username': username, 'password': password, 'email': email})
        email_message.attach_alternative(html_template, "text/html")
        email_message.send()
        return True

    def request_notification_email(self, request, process_stage_approvers, ):
        pk_requestid = request.pk_requestid
        Notification.objects.filter(
            fk_requestid=pk_requestid).update(status=0)

        for process_stage_approver in process_stage_approvers:
            profileid = process_stage_approver.fk_profileid_id
            request_date = request.date
            first_name = process_stage_approver.fk_profileid.user.first_name
            last_name = process_stage_approver.fk_profileid.user.last_name
            email = process_stage_approver.fk_profileid.user.email
          
            workflow = request.fk_processid.process
            workflow_id = request.workflow_id
            process_code = request.fk_processid.process_code
            process = request.fk_processid.process
            requested_first_name = request.fk_profileid.user.first_name
            requested_last_name = request.fk_profileid.user.last_name
            url = UrlHelper.view_url(
                self, process_code)
        

            notification = Notification()
            notification.fk_requestid_id = pk_requestid
            notification.name = first_name
            notification.profile_id = profileid
            notification.process = workflow
            notification.workflow = workflow_id
            notification.process_code = process_code
            notification.requested_by = requested_first_name + \
                " "+(requested_last_name).upper()
            

            notification.url = "https://tmldatapoint.web.app/#/" + \
                url+"/"+str(workflow_id)
            

            notification.date_created = datetime.now().strftime("%Y-%m-%d")
            notification.status = 1
            notification.save()

            with open(settings.BASE_DIR+"/templates/request_approval_email.txt") as txt_message:
                request_approval_message = txt_message.read()+" Firstname: " + \
                    first_name + " Email: "+email
            email_message = EmailMultiAlternatives(
                'Datapoint Request ('+process+')', request_approval_message, 'totaldatapoint@gmail.com', to=[email])
            html_templete = get_template("request_approval_email.html").render(
                {'approver': first_name, 'process': process, 'url': url+'/'+str(workflow_id), 'requested_by': requested_first_name+" "+requested_last_name, 'date': request_date})
            email_message.attach_alternative(html_templete, "text/html")
            email_message.send()

    def approved_request_notification_email(self, request):
        pk_requestid = request.pk_requestid
        profileid = request.fk_profileid_id
        first_name = request.fk_profileid.user.first_name
        last_name = request.fk_profileid.user.last_name

        email = request.fk_profileid.user.email
  
        request_date = request.date

        workflow = request.fk_processid.process
        workflow_id = request.workflow_id
        process_code = request.fk_processid.process_code
        process = request.fk_processid.process

        url = UrlHelper.view_url(
            self, process_code)

        Notification.objects.filter(fk_requestid=pk_requestid).update(status=0)
        notification = Notification()
        notification.fk_requestid_id = pk_requestid
        notification.name = first_name
        notification.profile_id = profileid
        notification.process = workflow
        notification.workflow = workflow_id
        notification.process_code = process_code
        notification.requested_by = first_name + " "+(last_name).upper()
        notification.url = "https://tmldatapoint.web.app/#/" + \
            url+"/"+str(workflow_id)
        notification.date_created = datetime.now().strftime("%Y-%m-%d")
        notification.status = 0
        notification.save()

        with open(settings.BASE_DIR+"/templates/request_approved_email.txt") as txt_message:
            request_approval_message = txt_message.read()+" Firstname: " + \
                first_name + " Email: "+email
        email_message = EmailMultiAlternatives(
            'Datapoint Request Approved ('+process+')', request_approval_message, 'totaldatapoint@gmail.com', to=[email])
        html_templete = get_template("request_approved_email.html").render(
            {'requested_by': first_name, 'process': process, 'url': url+'/'+str(workflow_id), 'date': request_date})
        email_message.attach_alternative(html_templete, "text/html")
        email_message.send()

    def reject_request_notification_email(self, request):
        pk_requestid = request.pk_requestid
        profileid = request.fk_profileid_id
        first_name = request.fk_profileid.user.first_name
        last_name = request.fk_profileid.user.last_name

        email = request.fk_profileid.user.email
        request_date = request.date

        workflow = request.fk_processid.process
        workflow_id = request.workflow_id
        process_code = request.fk_processid.process_code
        process = request.fk_processid.process

        url = UrlHelper.view_url(
            self, process_code)

        Notification.objects.filter(fk_requestid=pk_requestid).update(status=0)
        notification = Notification()
        notification.fk_requestid_id = pk_requestid
        notification.name = first_name
        notification.profile_id = profileid
        notification.process = workflow
        notification.workflow = workflow_id
        notification.process_code = process_code
        notification.requested_by = first_name + " "+(last_name).upper()
        notification.url = "https://tmldatapoint.web.app/#/" + \
            url+"/"+str(workflow_id)
        notification.date_created = datetime.now().strftime("%Y-%m-%d")
        notification.status = 0
        notification.save()

        with open(settings.BASE_DIR+"/templates/request_rejected_email.txt") as txt_message:
            request_approval_message = txt_message.read()+" Firstname: " + \
                first_name + " Email: "+email
        email_message = EmailMultiAlternatives(
            'Datapoint Request Rejected ('+process+')', request_approval_message, 'totaldatapoint@gmail.com', to=[email])
        html_templete = get_template("request_rejected_email.html").render(
            {'requested_by': first_name, 'process': process, 'url': url+'/'+str(workflow_id), 'date': request_date})
        email_message.attach_alternative(html_templete, "text/html")
        email_message.send()

    def password_reset(instance, password):
        with open(settings.BASE_DIR+"/templates/password_reset_email.txt") as txt_message:
            user_registration_message = txt_message.read()+" Username: "+instance.username + \
                " Email: "+instance.email + "Password: "+password
        email_message = EmailMultiAlternatives(
            'Datapoint Password Reset', user_registration_message, 'totaldatapoint@gmail.com', to=[instance.email])
        html_templete = get_template("password_reset_email.html").render(
            {'username': instance.username, 'password': password})
        email_message.attach_alternative(html_templete, "text/html")
        email_message.send()

    def helpdesk_admin_notification(helpdesk_admins, issue):
        url = 'https://tmldatapoint.web.app/#/helpdesk/' + \
            str(issue.pk_helpdeskid)
        requested_by = issue.fk_profileid.user.first_name + \
            " " + issue.fk_profileid.user.last_name
        request_date = issue.created_date
        issue = issue.issue

        for helpdesk_admin in helpdesk_admins:
            first_name = helpdesk_admin.fk_profileid.user.first_name
            firstname = helpdesk_admin.fk_profileid.user.first_name
            last_name = helpdesk_admin.fk_profileid.user.last_name
            email = helpdesk_admin.fk_profileid.user.email

            with open(settings.BASE_DIR+"/templates/helpdesk_admin_email.txt") as txt_message:
                request_approval_message = txt_message.read()+" Firstname: " + \
                    first_name + " Email: "+email
            email_message = EmailMultiAlternatives(
                'Datapoint Helpdesk Request', request_approval_message, 'totaldatapoint@gmail.com', to=[email])
            html_templete = get_template("helpdesk_admin_email.html").render(
                {'firstname': firstname, 'requested_by': requested_by, 'issue': issue, 'url': url, 'request_date': request_date})
            email_message.attach_alternative(html_templete, "text/html")
            email_message.send()

    def helpdesk_admin_notification(helpdesk_admins, issue):
        url = 'https://tmldatapoint.web.app/#/helpdesk/' + \
            str(issue.pk_helpdeskid)
        requested_by = issue.fk_profileid.user.first_name + \
            " " + issue.fk_profileid.user.last_name
        request_date = issue.created_date
        issue = issue.issue

        for helpdesk_admin in helpdesk_admins:
            first_name = helpdesk_admin.fk_profileid.user.first_name
            firstname = helpdesk_admin.fk_profileid.user.first_name
            last_name = helpdesk_admin.fk_profileid.user.last_name
            email = helpdesk_admin.fk_profileid.user.email
          


            print(helpdesk_admin.fk_profileid.user.email)
         

            with open(settings.BASE_DIR+"/templates/helpdesk_admin_email.txt") as txt_message:
                request_approval_message = txt_message.read()+" Firstname: " + \
                    first_name + " Email: "+email
            email_message = EmailMultiAlternatives(
                'Datapoint Helpdesk Issue', request_approval_message, 'totaldatapoint@gmail.com', to=[email])
            html_templete = get_template("helpdesk_admin_email.html").render(
                {'firstname': firstname, 'requested_by': requested_by, 'issue': issue, 'url': url, 'request_date': request_date})
            email_message.attach_alternative(html_templete, "text/html")
            email_message.send()
           
          

    def helpdesk_status_notification(helpdesk_admins, status):
        url = 'https://tmldatapoint.web.app/#/helpdesk/' + \
            str(status.fk_helpdeskid.pk_helpdeskid)
        requested_by = status.fk_helpdeskid.fk_profileid.user.first_name + \
            " " + status.fk_helpdeskid.fk_profileid.user.last_name
        request_date = status.fk_helpdeskid.created_date
        request_email = status.fk_helpdeskid.fk_profileid.user.email
        issue = status.fk_helpdeskid.issue
        comment = status.comment

        for helpdesk_admin in helpdesk_admins:
            first_name = helpdesk_admin.fk_profileid.user.first_name
            firstname = helpdesk_admin.fk_profileid.user.first_name
            last_name = helpdesk_admin.fk_profileid.user.last_name
            email = helpdesk_admin.fk_profileid.user.email

            with open(settings.BASE_DIR+"/templates/helpdesk_status_email.txt") as txt_message:
                request_approval_message = txt_message.read()+" Firstname: " + \
                    first_name + " Email: "+email
            email_message = EmailMultiAlternatives(
                'Datapoint Helpdesk Issue Status Update', request_approval_message, 'totaldatapoint@gmail.com', to=[email])
            html_templete = get_template("helpdesk_status_email.html").render(
                {'firstname': firstname, 'requested_by': requested_by, 'issue': issue, 'comment': comment, 'url': url, 'request_date': request_date})
            email_message.attach_alternative(html_templete, "text/html")
            email_message.send()

        with open(settings.BASE_DIR+"/templates/helpdesk_status_email.txt") as txt_message:
            request_approval_message = txt_message.read()+" Firstname: " + \
                requested_by + " Email: "+request_email
        email_message = EmailMultiAlternatives(
            'Datapoint Helpdesk Issue Status Update', request_approval_message, 'totaldatapoint@gmail.com', to=[request_email])
        html_templete = get_template("helpdesk_status_email.html").render(
            {'firstname': firstname, 'requested_by': requested_by, 'issue': issue, 'comment': comment, 'url': url, 'request_date': request_date})
        email_message.attach_alternative(html_templete, "text/html")
        email_message.send()
