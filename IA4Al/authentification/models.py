from django.db import models
from django.contrib.auth.models import AbstractUser
from authentification.file_limit import ContentTypeRestrictedFileField

class Utilisateur(AbstractUser):
    photo = models.ImageField()

class UploadFile(models.Model):
    # id=models.IntegerField()
    upload_file = ContentTypeRestrictedFileField(
        upload_to='fichiers/',
        content_types=['application/csv'],
        max_upload_size=5242880, blank=True, null=True)   
# Create your models here.
