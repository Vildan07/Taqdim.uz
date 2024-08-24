import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings
from django.core.mail import send_mail
import random
def generate_qr_code(profile):
    url = f"{settings.BASE_URL}/{profile.username}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    file_name = f'{profile.user.username}_qr.png'
    return File(buffer, name=file_name)


def generate_code():
    return random.randint(10000, 99999)





def send_email(subject, message, recipient_list, from_email=None):
    """
    A utility function to send an email.

    :param subject: Subject of the email
    :param message: Body of the email
    :param recipient_list: List of recipient email addresses
    :param from_email: (Optional) From email address, defaults to settings.DEFAULT_FROM_EMAIL
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,  # Set to True if you don't want exceptions raised on failure
    )

# send_email("Test!", 'Assalomu alaykum!', ['deeorback@gmail.com'])