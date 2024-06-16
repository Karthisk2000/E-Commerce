from django.db import models


class UserDetails(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    image = models.ImageField(null=True,blank=True)
    description = models.CharField(max_length=400,null=True)

    def __str__(self):
        return self.name