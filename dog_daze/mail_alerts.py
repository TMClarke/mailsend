import json
import os
import urllib2
from sendgrid.helpers.mail import *
from sendgrid import *

def send_confirmation(email_addr, username):
    mail = Mail()

    mail.from_email = Email("signup@dogdaze.io", "Dog Daze Admin")
    mail.subject = "[Confirmation] - Thanks for signing up to Dog Daze!"

    mail.template_id = "0l5k1c9u-35lm-00an-8b1t-p8gk3f2621oo"

    personalization = Personalization()
    personalization.add_to(email_addr)
    personalization.add_substitution("%username%", username)

    personalization.add_substitution("%email%", email)

    mail.add_personalization(personalization)

    sg = SendGridAPIClient(username=os.environ.get('USERNAME'),
                           password=os.environ.get('PASSWORD'))

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.headers)
        print(response.body)
    except:
        Exception("SendGrid send failed - please check API usage.")
