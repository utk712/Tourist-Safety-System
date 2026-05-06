from django.db import models

class Incident(models.Model):
    tourist_name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tourist_name