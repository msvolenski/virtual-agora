# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.conf import settings
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
#from agoraunicamp.models import Projeto

def getProject():
    try:
        choices =[ (o.sigla, o.sigla) for o in Projeto.objects.all()]
    except:
        choices = [("Default", "Default")]
    return choices


#projeto
class Article(models.Model):

    projeto = models.ForeignKey('projetos.Projeto')
    title = models.CharField('Título do artigo',max_length=200)
    tags = TaggableManager()
    article = RichTextUploadingField(config_name='default', verbose_name=u'Descrição')
    publ_date = models.DateTimeField('Data de publicação')
    destaque = models.CharField('Destacado?',max_length=3, default='Não')
    questao_associada = models.CommaSeparatedIntegerField(max_length=100, blank=True)
    address = models.CharField('Endereço',max_length=200)
    published = models.CharField('Publicado?',max_length=3, default='Não')

    def __str__(self):
        return self.title.encode('utf8')

    def split_numbers(self):
        return self.questao_associada.split(',')

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        self.address = "{SITE_URL}agora/conheca/artigos/{id}".format(id=self.id, SITE_URL=settings.SITE_URL)
        return super(Article, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'


#projeto
class Topico(models.Model):
  projeto = models.ForeignKey('projetos.Projeto')
  topico = models.CharField(max_length=200)
  address_topico = models.CharField(max_length=200)
  position = models.IntegerField(default=1)

  def __str__(self):
    return self.topico.encode('utf8')

  def __int__(self):
    return self.position

  class Meta:
      verbose_name = 'Tópico'
      verbose_name_plural = 'Tópicos'

  def save(self, *args, **kwargs):
      super(Topico, self).save(*args, **kwargs)
      self.address_topico = "{SITE_URL}agora/conheca/topicos/{id}".format(id=self.id,SITE_URL=settings.SITE_URL)
      return super(Topico, self).save(*args, **kwargs)

#projeto-forignekey
class SubTopico(models.Model):
  subtopico = models.ForeignKey(Topico, on_delete=models.CASCADE)
  subtopico_nome = models.CharField(max_length=200)

  def __str__(self):
    return "%s %s" % (self.subtopico, self.subtopico_nome.encode('utf8'))

  class Meta:
      verbose_name = 'Sub-topico'
      verbose_name_plural = 'Sub-tópicos'

class Link(models.Model):
  title = models.ForeignKey(SubTopico, on_delete=models.CASCADE)
  url = models.URLField(max_length=1000)
  url_title = models.CharField(max_length=1000)

  def __str__(self):
    return self.url
