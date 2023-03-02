from django.db import models

# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    age = models.IntegerField()

    # dunder str method return cat name
    def __str__(self):
        return self.name