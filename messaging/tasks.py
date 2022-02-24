from celery import shared_task
from .mail_utils import SendMail

@shared_task(name="Send Email")
def send_email(
    mail_for,
    recipient_name, 
    link,
    recipient_list,
    subject):

    mail = SendMail(
        mail_for=mail_for,
        recipient_name=recipient_name,
        link=link,
        recipient_list=recipient_list,
        subject=subject,
    )
    status = mail.send()

    return True


