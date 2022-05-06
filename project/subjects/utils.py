from django.conf import settings
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string

def send_faculty_allocation_mail(mail_list):
	emails = []
	for mail in mail_list:
		# Sending welcome mail
		role = mail['role']
		subject = mail['subject']
		user_email = mail['email']
		subject = f'You have been alloted as {role} to {subject}!'
		body = render_to_string('emails/faculty_allocation_mail.html', mail)
		email = (subject, body, settings.EMAIL_HOST_USER, [user_email])
		emails.append(email)
	emails = tuple(emails)
	sent_mails = send_mass_mail(emails, fail_silently=False)
	print(f'Out of {len(emails)}, {sent_mails} has been sent!')