from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Projeto(models.Model):
    projeto = models.CharField('Projeto',max_length=100,blank=True, null=True)
    sigla = models.CharField('Sigla',max_length=50,blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.sigla, self.projeto)
