import base64
from django.core.files.base import ContentFile


def convert_image_base64_to_file(data, name):
    
    img_format, img_str = data.split(';base64,')
    ext = img_format.split('/')[-1]

    data = ContentFile(base64.b64decode(img_str), name=name + '.' + ext)
    return data