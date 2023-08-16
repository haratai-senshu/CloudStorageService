from django.db import models
from django.urls import reverse_lazy
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone

class Post(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=False,
        null=False)

    user_name = models.CharField(default=256,max_length=256,blank=False,null=False)

    file_name = models.FileField(blank=False, null=False, verbose_name='ファイル')

    def get_absolute_url(self):
        return reverse_lazy("detail", args=[self.id])
