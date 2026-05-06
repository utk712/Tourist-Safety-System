from django.db import models

class Tourist(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name