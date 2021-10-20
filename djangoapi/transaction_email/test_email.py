# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

BASE_URL="https://www.technicallycpa.com/"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'admin@technicallycpa.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'CPA Tech <admin@technicallycpa.com>'
SENDGRID_API_KEY=os.environ.get('SENDGRID_API_KEY')


message = Mail(
    from_email=EMAIL_HOST_USER,
    to_emails='kyle.callaway@att.net',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)