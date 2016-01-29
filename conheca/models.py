from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
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
        
        
class Article(models.Model):
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    tags = TaggableManager()
    article = models.TextField()
    reference = models.CharField(max_length=200)
    destaque = models.CharField(max_length=3, default='Não')    
    questao_associada = models.CommaSeparatedIntegerField(max_length=100, blank=True)  
    
    def __str__(self):
        return self.title
        
    def split_numbers(self):
        return self.questao_associada.split(',')