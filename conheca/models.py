﻿from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from tinymce.models import HTMLField


class Article(models.Model):    
    
    title = models.CharField('Título do artigo',max_length=200)    
    tags = TaggableManager()
    article = RichTextUploadingField(config_name='default', verbose_name=u'Descrição')
    publ_date = models.DateTimeField('Data de publicação')
    destaque = models.CharField('Destacado?',max_length=3, default='Não')    
    questao_associada = models.CommaSeparatedIntegerField(max_length=100, blank=True)  
    address = models.CharField('Endereço',max_length=200)
    published = models.CharField('Publicado?',max_length=3, default='Não')     
    
    def __str__(self):
        return self.title
        
    def split_numbers(self):
        return self.questao_associada.split(',')
        
    def save(self, *args, **kwargs): 
        super(Article, self).save(*args, **kwargs)                     
        self.address = "http://127.0.0.1:8000/agora/pdpu/conheca/artigos/{id}".format(id=self.id)       
        return super(Article, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'
        

class Topico(models.Model):
 

  def position_det():
    try:
      tpc = Topico.objects.latest('position')
    except (KeyError, Topico.DoesNotExist):
      return 1
    a = tpc.position
    a = a + 1
    return a
    
  
  topico = models.CharField(max_length=200)
  address_topico = models.CharField(max_length=200)
  position = models.IntegerField(default=position_det) 

  def __str__(self):
    return self.topico

  def __int__(self):
    return self.position
    
  class Meta:
      verbose_name = 'Tópico'
      verbose_name_plural = 'Tópicos'
      
  def save(self, *args, **kwargs): 
      super(Topico, self).save(*args, **kwargs)                     
      self.address_topico = "http://127.0.0.1:8000/agora/pdpu/conheca/topicos/{id}".format(id=self.id)
      return super(Topico, self).save(*args, **kwargs)

class SubTopico(models.Model):
  subtopico = models.ForeignKey(Topico, on_delete=models.CASCADE)
  subtopico_nome = models.CharField(max_length=200)

  def __str__(self):
    return "%s %s" % (self.subtopico, self.subtopico_nome)
    
  class Meta:
      verbose_name = 'Sub-topico'
      verbose_name_plural = 'Sub-tópicos'

class Link(models.Model):
  title = models.ForeignKey(SubTopico, on_delete=models.CASCADE)
  url = models.URLField(max_length=1000)
  url_title = models.CharField(max_length=1000)

  def __str__(self):
    return self.url
