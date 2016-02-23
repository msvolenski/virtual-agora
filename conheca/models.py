from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from tinymce.models import HTMLField


class Article(models.Model):

    
    
    title = models.CharField(max_length=200)    
    tags = TaggableManager()
    article = RichTextUploadingField(config_name='full', verbose_name=u'Descrição')
    publ_date = models.DateTimeField()
    destaque = models.CharField(max_length=3, default='Não')    
    questao_associada = models.CommaSeparatedIntegerField(max_length=100, blank=True)  
    address = models.CharField(max_length=200)
    published = models.CharField(max_length=3, default='Não')     
    
    def __str__(self):
        return self.title
        
    def split_numbers(self):
        return self.questao_associada.split(',')
        
    def save(self, *args, **kwargs): 
        super(Article, self).save(*args, **kwargs)                     
        self.address = "http://127.0.0.1:8000/agora/pdpu/conheca/artigos/{id}".format(id=self.id)
       
        return super(Article, self).save(*args, **kwargs)
        

class Topico(models.Model):
  topico = models.CharField(max_length=200)

  def get_address_topico():
    try:
      tpc = Topico.objects.latest('id')
    except (KeyError, Topico.DoesNotExist):
      return str('http://127.0.0.1:8000/agora/pdpu/conheca/topicos/') + str(1)
    a = tpc.pk
    a = a + 1
    return str('http://127.0.0.1:8000/agora/pdpu/conheca/topicos/') + str(a)

  def position_det():
    try:
      tpc = Topico.objects.latest('position')
    except (KeyError, Topico.DoesNotExist):
      return 1
    a = tpc.position
    a = a + 1
    return a

  address_topico = models.CharField(max_length=200, default=get_address_topico)
  position = models.IntegerField(default=position_det)

  def __str__(self):
    return self.topico

  def __int__(self):
    return self.position

class SubTopico(models.Model):
  subtopico = models.ForeignKey(Topico, on_delete=models.CASCADE)
  subtopico_nome = models.CharField(max_length=200)

  def __str__(self):
    return "%s %s" % (self.subtopico, self.subtopico_nome)

class Link(models.Model):
  title = models.ForeignKey(SubTopico, on_delete=models.CASCADE)
  url = models.URLField(max_length=1000)
  url_title = models.CharField(max_length=1000)

  def __str__(self):
    return self.url
