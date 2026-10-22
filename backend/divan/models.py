from django.db import models

# Create your models here.

class Poet(models.Model):
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)
    century = models.IntegerField(blank=True, null=True)

class Poem(models.Model):
    poet = models.ForeignKey(Poet, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    poem_type = models.CharField(max_length=20, default='غزل')

class Verse(models.Model):
    verse = models.ForeignKey(Poem, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, null=True)
    first_couplet = models.CharField(max_length=255)
    second_couplet = models.CharField(max_length=255)