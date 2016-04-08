# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User as AuthUser
from django.utils import timezone
from taggit.managers import TaggableManager
from forum.models import User as Userf
from django.core.exceptions import ObjectDoesNotExist
#from agora.models import Choice


# Create your models here.

class User(models.Model):
  user = models.OneToOneField(
    AuthUser,
    primary_key=True,
    parent_link=True,

  )

  STAFF_TYPE = (
      ('1', 'Professor'),
      ('2', 'Funcionário'),
      ('3', 'Aluno'),
      ('4', 'Outro'),
  )

  primeiro_nome =  models.CharField('Primeiro nome', max_length=40, blank=True)
  ultimo_nome =  models.CharField('Sobrenome', max_length=100, blank=True)
  staff = models.CharField('Staff', max_length=1, blank=True, choices = STAFF_TYPE)
  year_of_start = models.IntegerField('Ano de ingresso',blank=True, default='9999')
  course = models.CharField('Curso', max_length=40, blank=True , default='curso')
  institute = models.CharField('Instituto', max_length=40, blank=True, default='instituto')
  academic_registry = models.IntegerField('Registro acadêmico',default='9999')
  email = models.EmailField('Email', blank=True)
  nickname = models.CharField('Apelido',max_length=40, blank=True)
  question_answer = models.ManyToManyField(
    'agora.question',
    #Question,   #verificar
    through='Answer',
    through_fields=('user', 'question'),
    related_name='question_answer',
  )

  class Meta:
    verbose_name = 'usuário'
    verbose_name_plural = 'usuários'

  def save(self, *args, **kwargs):
      super(User, self).save(*args, **kwargs)
      nome = self.user.user
      try:
         Termo.objects.get(user=nome)
      except:
         Termo.objects.create(user=self)
         Userf.objects.create(user=self.user)
         a = Userf.objects.get(user=self.user)
         a.username="{A} {B}".format(A=self.primeiro_nome,B=self.ultimo_nome)
         a.save()
         return super(User, self).save(*args, **kwargs)
      return super(User, self).save(*args, **kwargs)



class Answer(models.Model):
  user = models.ForeignKey(User, related_name='user_answer')
  question = models.ForeignKey('agora.Question',related_name='question')
  choice = models.ForeignKey('agora.Choice', related_name='choice', blank=True, null=True)
  text = models.TextField(max_length=200, blank=True, null=True)
  answer_date = models.DateTimeField(editable=False)

  def __str__(self):
    if self.choice:
      return self.choice.choice_text
    return self.text

  def save(self, *args, **kwargs):
    """On save, update timestamps"""

    if not self.id:
      self.answer_date = timezone.now()
    return super(Answer, self).save(*args, **kwargs)

  def user_dept(self):
    return self.user.department
  user_dept.short_description = 'Faculdade'

  def userd(self):
    return self.user.user

  class Meta:
    verbose_name = 'resposta'
    verbose_name_plural = 'respostas'


class Termo(models.Model):
    user = models.ForeignKey(User, related_name='user_termo')
    condition = models.CharField('Condição', max_length=3, default='Não')

    def __str__(self):
        return self.condition

    def userd(self):
        return self.user.user


class MeuEspaco(models.Model):

    user = models.CharField('Usuario',max_length=200, blank=True)
    categoria = models.CharField('Categoria',max_length=20, blank=True)
    publ_date = models.DateTimeField('Data de publicação')
    link =  models.URLField(max_length=1000, blank=True)
    comentario =  models.CharField('Comentário',max_length=200, blank=True)
    secao = models.CharField('Seção',max_length=30, blank=True)
    arquivo = models.FileField (upload_to = settings.MEDIA_ROOT, max_length=2000000, blank=True)
