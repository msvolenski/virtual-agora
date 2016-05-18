# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.contrib.auth.models import User as AuthUser
from django.utils import timezone
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField



#PROJETO
class Category(models.Model):
  """Model for types of subjects"""
  projeto = models.ForeignKey('projetos.Projeto', max_length=50, blank=False)
  title = models.CharField(max_length=50)
  tags = TaggableManager()

  def __str__(self):
    return self.title.encode('utf8')

  class Meta:
    verbose_name = 'categoria'
    verbose_name_plural = 'categorias'




class Topic(models.Model):
  """Model for topics of a theme"""

  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  title = models.CharField('Título', max_length=50)
  text = RichTextUploadingField(config_name='default', verbose_name=u'Texto')
  publ_date = models.DateTimeField('Data de publicação')
  tags = TaggableManager()
  published = models.CharField('Publicado?',max_length=3, default='Não')
  projeto = models.ForeignKey('projetos.Projeto', max_length=50, blank=False)

  def __str__(self):
    return self.title.encode('utf8')

  def save(self, *args, **kwargs):
    """On save, update timestamps"""
    if not self.id:
      self.publ_date = timezone.now()
    return super(Topic, self).save(*args, **kwargs)

  class Meta:
    verbose_name = 'tópico'
    verbose_name_plural = 'tópicos'


class User(models.Model):
  """Extends User model from Authentication app"""
  username = models.CharField(max_length=50, default="username")
  user = models.OneToOneField(
    AuthUser,
    primary_key=True,
    parent_link=True,
    related_name='topic_user',
  )
  topic_answer = models.ManyToManyField(
    Topic,
    through='TopicAnswer',
    through_fields=('user', 'topic'),
    related_name='topic_answer',
  )
  topic_answer_like = models.ManyToManyField(
    'TopicAnswer',
    through='Like',
    through_fields=('user', 'answer'),
    related_name='topic_answer_like',
  )

  def __str__(self):
    return self.username


  class Meta:
    verbose_name = 'usuário'
    verbose_name_plural = 'usuários'




class TopicAnswer(models.Model):
  """Answer to a topic"""

  user = models.ForeignKey(User)
  topic = models.ForeignKey(Topic)
  text = RichTextUploadingField(config_name='full', verbose_name='')
  answer_date = models.DateTimeField(editable=False)

  def __str__(self):
    return self.text

  def save(self, *args, **kwargs):
    """On save, update timestamps"""

    if not self.id:
      self.answer_date = timezone.now()
    return super(TopicAnswer, self).save(*args, **kwargs)

  class Meta:
    verbose_name = 'resposta'
    verbose_name_plural = 'respostas'


class TopicAnswerForm(forms.ModelForm):
  class Meta:
    model = TopicAnswer
    fields = ['text']


class Like(models.Model):
  "Like to an answer"

  user = models.ForeignKey(User)
  answer = models.ForeignKey(TopicAnswer)

  class Meta:
    verbose_name = 'curtir'
    verbose_name_plural = 'curtires'
