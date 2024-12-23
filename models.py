from django.db import models

# Create your models here.

class reg(models.Model):
    fullname = models.CharField(max_length=20)
    mail = models.EmailField()
    password = models.CharField(max_length=20)

class scam(models.Model):
    urls = models.CharField(max_length=500)
    category = models.CharField(max_length=500)
    domain = models.CharField(max_length=500)


class notifications(models.Model):
    data = models.CharField(max_length=500)


class feedback(models.Model):
    Name = models.CharField(max_length=20)
    Mail = models.EmailField()
    Phone = models.IntegerField()
    Message = models.CharField(max_length=500)



class scammodel(models.Model):
    urls = models.CharField(max_length=500)
    category = models.CharField(max_length=500)
    status=models.CharField(max_length=50)
