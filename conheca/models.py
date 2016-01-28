from django.db import models
from django.utils import timezone
# Create your models here.


class AdicionaLink(models.Model):


    titulo = models.CharField(max_length=200)
    url = models.CharField(max_length=1000)

    data_publicacao = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.data_publicacao = timezone.now()
        self.save()

    def __str__(self):
        return self.titulo