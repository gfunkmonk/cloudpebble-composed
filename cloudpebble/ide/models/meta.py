from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class IdeModel(models.Model):
    class Meta(object):
        abstract = True
        app_label = "ide"


@receiver(pre_save)
def pre_save_full_clean_handler(sender, instance, *args, **kwargs):
    """ Force IdeModels to call full_clean before save """
    if isinstance(instance, IdeModel):
        instance.full_clean()
