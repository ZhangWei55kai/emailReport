# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#权限表
class Permis(models.Model):
    name = models.CharField(blank=True,max_length=30)
    url = models.CharField(blank=True,max_length=30)

class User(AbstractUser):
    Permis = models.ManyToManyField(Permis)




