from celery import shared_task

from django.core.files.base import ContentFile

from .models import AppFile

# Image processing stuff
from io import BytesIO
from PIL import Image

@shared_task(name="Process Image Thumbnails")
def process_image_thumbnails(app_file_id):

    app_file = AppFile.objects.filter(id=app_file_id).first()

    if not app_file:
        return

    print('--> Processing image thumbnail')
    image = Image.open(app_file.file)
    basewidth = 500  # Thumbnail size
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image.thumbnail((basewidth, hsize), Image.ANTIALIAS)
    print('--> Thumbnail generated')

    # Save the thumbnail
    temp_handle = BytesIO()
    image.save(temp_handle, format=image.format)
    app_file.thumbnail.save('thumb_' + randomfilestr() + app_file.file_extension,
                                   ContentFile(temp_handle.getvalue()))

    print('--> Thumbnail saved')

    print('--> Processing image micro thumbnail')
    image = Image.open(app_file.file)
    basewidth = 200  # Thumbnail size
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image.thumbnail((basewidth, hsize), Image.ANTIALIAS)
    print('--> Micro thumbnail generated')

    # Save the thumbnail
    temp_handle = BytesIO()
    image.save(temp_handle, format=image.format)
    app_file.micro_thumbnail.save('micro_' + randomfilestr() + app_file.file_extension,
                                   ContentFile(temp_handle.getvalue()))

    print('--> Micro thumbnail saved')

    return True


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))