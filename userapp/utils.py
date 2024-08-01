import qrcode
from io import BytesIO
from django.core.files import File


def generate_qr_code(profile):
    url = f"http://taqdim.uz/{profile.user.username}"
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