from django.db import models
from .storage_config import *

class AppFile(models.Model):
    id = models.AutoField(primary_key=True)
    display_id = models.CharField(editable=False, max_length=16, null=False)
    file = models.FileField(upload_to='uploads/', storage=PrivateMediaStorage())
    thumbnail = models.FileField(upload_to='uploads/', storage=PrivateMediaStorage(), null=True)
    micro_thumbnail = models.FileField(upload_to='uploads/', storage=PrivateMediaStorage(), null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    file_name = models.CharField(max_length=200, null=True)
    file_size = models.IntegerField(null=True)
    file_type = models.CharField(max_length=50, null=True)
    file_extension = models.CharField(max_length=25, null=True)

    FILE_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=FILE_STATUS,
        blank=False,
        default='active',
    )