from django.db import models

# Create your models here.
class Dict(models.Model):
    text = models.CharField(max_length=1024, unique=True)
    translation = models.CharField(max_length=1024, unique=True)

    def __unicode__(self):
        return self.text
