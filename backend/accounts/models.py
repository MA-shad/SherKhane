from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class poet(models.Model):
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)
    century = models.IntegerField(blank=True, null=True)

class poem(models.Model):
    poet = models.ForeignKey(poet, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    poem_type = models.CharField(max_length=20, default='غزل')

class verse(models.Model):
    verse = models.ForeignKey(poem, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, null=True)
    first_couplet = models.CharField(max_length=255)
    second_couplet = models.CharField(max_length=255)

