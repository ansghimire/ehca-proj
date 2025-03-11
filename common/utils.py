import uuid
import random 
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings


class GenerateKey:
    @staticmethod
    def return_value():
        key = str(random.randint(100000, 999999))
        return key


def generate_unique_id():
    return str(uuid.uuid4())


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_verification_email(email, otp):
    email_template = render_to_string('../templates/signup_otp.html', {"otp": otp, "username": email})    
    sign_up = EmailMultiAlternatives(
        "Otp Verification", 
        "Otp Verification",
        settings.EMAIL_HOST_USER, 
        [email],
    )
    sign_up.attach_alternative(email_template, 'text/html')
    sign_up.send()


def send_activation_success_email(user_email):
    # Rendering the email template
    email_template = render_to_string('signup_success.html', {"username": user_email})

    # Creating and sending the email
    sign_up = EmailMultiAlternatives(
        "Account successfully activated", 
        "Account successfully activated",
        settings.EMAIL_HOST_USER, 
        [user_email],
    )
    sign_up.attach_alternative(email_template, 'text/html')
    sign_up.send()
    
