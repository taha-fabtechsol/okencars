from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

from app import choices, models

import threading

def send_forgot_password_token(user: models.User):
    otp = user.confirmation_token
    send_mail("Forgot password token...", f"Use this OTP: {otp} to reset your password.", settings.EMAIL_HOST_USER, [user.email])


def send_password_update_success_email(user):
    message = f"""
Dear {user.first_name.title()},

This is a confirmation that the password for your account has been successfully changed.

If you did not request this change or need further assistance, please contact our support team immediately.

Thank you for choosing our service.

Best regards,
MPRUV team
    """
    send_mail("Password updated successfully!", message, settings.EMAIL_HOST_USER, [user.email])


def send_html_email(subject, html_template, context, recipient_list):
    def send(subject, html_template, context, recipient_list):
        html_message = render_to_string(html_template, context)
        plain_message = strip_tags(html_message)
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            html_message=html_message,
        )
    task = threading.Thread(target=send, args=(subject, html_template, context, recipient_list))
    task.start()


def send_welcome_mail(user: models.User, owner: models.User, password):
    context = dict(user=user) | dict(password=password) | dict(url=settings.FRONTEND_ADDRESS) | dict(owner=owner)
    subject = ""
    html_template = ""
    recipient_list = [user.email]
    
    if user.role == choices.UserRole.ADMIN:
        subject = "Welcome Aboard, Admin! Your Journey with OkenCars Begins Here"
        html_template = "emails/welcome_mail.html"
        
    elif user.role == choices.UserRole.MANAGER:
        subject = "Welcome to the OkenCars Team, Manager! Driving Success Together"
        html_template = "emails/welcome_mail.html"
        
    elif user.role == choices.UserRole.OWNER:
        subject = "Welcome, Owner! Empowering Your Fleet Management with OkenCars"
        html_template = "emails/welcome_mail.html"
        
    elif user.role == choices.UserRole.DRIVER:
        subject = "Welcome, Driver! Let's Hit the Road with OkenCars"
        html_template = "emails/welcome_mail.html"

    send_html_email(subject, html_template, context, recipient_list)
    
