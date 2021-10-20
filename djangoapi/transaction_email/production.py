import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'admin@technicallycpa.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'CPA Tech <admin@technicallycpa.com>'
SENDGRID_API_KEY=os.environ.get('SENDGRID_API_KEY')


"""
PY SHELL TEST - 
IMPORTS
from django.conf import settings
from django.core.mail import send_mail

TEST MSG
send_mail("subject","here is the message",settings.EMAIL_HOST_USER,["kyle.callaway@att.net"],fail_silently=False)

send_mail(
    "subject",
    "here is the message",
    settings.EMAIL_HOST_USER,
    ["kyle.callaway@att.net"],
    fail_silently=False
    )

send_mail(
    "subject",
    "here is the message",
    from_email,
    to_email_list, #must be a list []
    fail_silently=False
    )

"""
print(f"\nEMAIL_HOST_USER {EMAIL_HOST_USER}")