# virtuhire-backend/accounts/email.py

from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(email: str, code: str):
    send_mail(
        subject='Your VirtuHire verification code',
        message=f'Your OTP code is: {code}\n\nThis code expires in 10 minutes.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )


def send_registration_confirmation(email: str, name: str):
    send_mail(
        subject='Welcome to VirtuHire',
        message=f'Hi {name},\n\nYour account has been created successfully.\n\nYou can now sign contracts, browse candidates, and manage your team from your dashboard.\n\nBest regards,\nVirtuHire Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )


def send_contract_signed(email: str, name: str):
    send_mail(
        subject='Contract Signed — VirtuHire',
        message=f'Hi {name},\n\nYour service agreement has been signed successfully. A PDF copy is available in your dashboard.\n\nBest regards,\nVirtuHire Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )


def send_interview_request_notification(client_email: str, candidate_name: str, client_name: str):
    # Notify VirtuHire team
    send_mail(
        subject=f'Interview Request — {candidate_name}',
        message=f'Client {client_name} has requested an interview with {candidate_name}.\n\nPlease schedule the interview and update the status in the admin panel.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=True,
    )
    # Notify client
    send_mail(
        subject='Interview Request Received — VirtuHire',
        message=f'Hi {client_name},\n\nYour interview request for {candidate_name} has been received. Our team will contact you within 24 hours to schedule.\n\nBest regards,\nVirtuHire Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[client_email],
        fail_silently=True,
    )


def send_hire_confirmation(client_email: str, client_name: str, candidate_name: str, role: str, monthly_rate: int):
    send_mail(
        subject=f'Hire Confirmed — {candidate_name} is now Active',
        message=f'Hi {client_name},\n\nCongratulations! {candidate_name} ({role}) is now active on your account.\n\nMonthly rate: {monthly_rate:,} AED\n\nYou can manage your employee from your dashboard.\n\nBest regards,\nVirtuHire Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[client_email],
        fail_silently=True,
    )


def send_invoice_generated(client_email: str, client_name: str, invoice_number: str, amount: int):
    send_mail(
        subject=f'Invoice {invoice_number} — VirtuHire',
        message=f'Hi {client_name},\n\nYour invoice {invoice_number} for {amount:,} AED has been generated and is available for download in your dashboard.\n\nBest regards,\nVirtuHire Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[client_email],
        fail_silently=True,
    )


def send_candidate_application_received(email: str, name: str):
    send_mail(
        subject='Application Received — VirtuHire',
        message=f'Hi {name},\n\nThank you for applying to VirtuHire! Your application is currently under review.\n\nWe will notify you once your profile has been approved and is visible to GCC clients.\n\nBest regards,\nVirtuHire Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )


def send_candidate_approved(email: str, name: str):
    send_mail(
        subject='Profile Approved — VirtuHire',
        message=f'Hi {name},\n\nGreat news! Your profile has been approved and is now visible to GCC clients on VirtuHire.\n\nGood luck!\n\nBest regards,\nVirtuHire Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )