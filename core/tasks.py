from celery import shared_task
from django.core.mail import send_mail
from cgpu_connect import settings

@shared_task(bind=True)
def send_async_mail(self, to_addresses, subject, message):
    if settings.DISABLE_EMAIL:
        return f"Send email to f{to_addresses} with subject: {subject} and the message is '{message}'"
    send_mail(
        subject = subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=to_addresses,
        fail_silently=False,
        )
    return "Done"