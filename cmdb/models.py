from django.db import models

# Create your models here.
class gallery(models.Model):
    gallery_id = models.AutoField(max_length=11, null=False, primary_key=True)
    name = models.CharField(max_length=45, null=True)
    description = models.CharField(max_length=2000, null=True)

class artist(models.Model):
    artist_id = models.AutoField(max_length=11, null=False, primary_key=True)
    name = models.CharField(max_length=45, null=True)
    birth_year = models.IntegerField(max_length=11, null=True)
    country = models.CharField(max_length=45, null=True)
    description = models.CharField(max_length=45, null=True)

class detail(models.Model):
    detail_id = models.AutoField(max_length=11, null=False, primary_key=True)
    image_id = models.IntegerField(max_length=11, null=True)
    year = models.IntegerField(max_length=11, null=True)
    type = models.CharField(max_length=45, null=True)
    width = models.IntegerField(max_length=11, null=True)
    height = models.IntegerField(max_length=11, null=True)
    location = models.CharField(max_length=45, null=True)
    description = models.CharField(max_length=45, null=True)

class image(models.Model):
    image_id = models.AutoField(max_length=11, null=False, primary_key=True)
    title = models.CharField(max_length=45, null=True)
    link = models.CharField(max_length=200, null=True)
    gallery_id = models.IntegerField(max_length=11, null=True)
    artist_id = models.IntegerField(max_length=11, null=True)
    detail_id = models.IntegerField(max_length=11, null=True)

class searchResult(models.Model):
    fileName = models.CharField(max_length=100, null=True)
    webLink = models.CharField(max_length=400, null=True)
    snippet = models.CharField(max_length= 400, null=True)