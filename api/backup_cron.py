from django.core.management import call_command
import subprocess as sp


def backup_db():
    try:
        sp.getoutput('python manage.py dbbackup')
    except:
        pass
