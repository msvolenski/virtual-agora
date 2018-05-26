# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.conf import settings
from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User as AuthUser
from django.utils import timezone
from taggit.managers import TaggableManager
from django.core.exceptions import ObjectDoesNotExist
from ckeditor_uploader.fields import RichTextUploadingField

class Projeto(models.Model):
    projeto = models.CharField('Projeto',max_length=100,blank=True, null=True)
    sigla = models.CharField('Sigla',max_length=50,blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.sigla, self.projeto)


class Topic(models.Model):
  title = models.CharField('Título', max_length=50)
  text = RichTextUploadingField(config_name='default', verbose_name=u'Texto')
  publ_date = models.DateTimeField('Data de publicação')
  tags = TaggableManager()
  published = models.CharField('Publicado?',max_length=3, default='Não')
  projeto = models.ForeignKey('Projeto', max_length=50, blank=False)

  def __str__(self):
    return self.title.encode('utf8')

  def save(self, *args, **kwargs):    
    if not self.id:
      self.publ_date = timezone.now()
    return super(Topic, self).save(*args, **kwargs)

  class Meta:
    verbose_name = 'debate'
    verbose_name_plural = 'debates'



class Question(models.Model):
    STATUS_CHOICES = (
        ('n', 'Não publicado'), # unpublished
        ('p', 'Publicado'),     # published
    )

    EXP_TIME = (
        (1, '1 dia'),           # a day
        (7, '1 semana'),        # a week
        (30, '1 mês'),          # a month
        (365, '1 ano'),         # a year
        (3650, 'Indeterminado') # undetermined
    )

    QUESTION_TYPE = (
        ('1', 'One choice'),
        ('2', 'Multipla Escolha'),
        ('3', 'Texto'),
    )

    projeto = models.ForeignKey('Projeto')
    question_type = models.CharField('Tipo', max_length=1, choices = QUESTION_TYPE)
    question_text = models.CharField('Título da Questão',max_length=200)
    publ_date = models.DateTimeField('Data de publicação')
    exp_date = models.DateTimeField('Data de expiração')
    days = models.IntegerField('Tempo para expirar', choices=EXP_TIME, default=3650)
    question_status = models.CharField('Estado da questão', max_length=1, choices=STATUS_CHOICES, default = 'n')
    answer_status = models.CharField('Estado da resposta', max_length=1, choices=STATUS_CHOICES, default = 'n')
    image = models.ImageField('Imagem', upload_to='question_images', blank=True, null=True)
    tags = TaggableManager()
    address = models.CharField('Endereço',max_length=200)
    permissao = models.IntegerField(default=0)
    resultado = models.CharField(max_length=1, choices=STATUS_CHOICES , default = 'n')


    def __str__(self):
        if self.id:
            return "#{id} - {question}".format(id=self.id, question=self.question_text.encode('utf8'))
        else:
            return self.question_text.encode('utf8')

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.publ_date = timezone.now()
        self.update_expiration_time()
        super(Question, self).save(*args, **kwargs)
        self.address = "{SITE_URL}agora/participe/{id}".format(id=self.id,SITE_URL=settings.SITE_URL)
        return super(Question, self).save(*args, **kwargs)

    def update_expiration_time(self):
        self.exp_date = self.publ_date + timedelta(days=self.days)

    def is_question_expired(self):
        return self.exp_date <= timezone.now()

    def is_question_published(self):
        if self.is_question_expired():
            self.question_status = 'n'
        if self.question_status == 'p':
            return True
        else:
            return False

    is_question_published.boolean = True
    is_question_published.short_description = 'Questão publicada?'

    def is_answer_published(self):
        if self.answer_status == 'p':
            return True
        else:
            return False

    is_answer_published.boolean = True
    is_answer_published.short_description = 'Resposta publicada?'

    class Meta:
        verbose_name = 'questão'
        verbose_name_plural = 'questões'



class User(models.Model):
  user = models.OneToOneField(
    AuthUser,
    primary_key=True,
    parent_link=True, 
  )

  STAFF_TYPE = (
      ('1', 'Professor'),
      ('2', 'Funcionario'),
      ('3', 'Aluno-Graduacao'),
      ('4', 'Aluno-Mestrado'),
      ('5', 'Aluno-Doutorado'),
      ('6', 'Aluno-Especial'),
      ('7', 'Aluno-Lato'),
      ('8', 'outro'),
  )

  primeiro_nome =  models.CharField('Primeiro nome', max_length=40, blank=True)
  ultimo_nome =  models.CharField('Sobrenome', max_length=100, blank=True)
  staff = models.CharField('Staff', max_length=1, blank=True, choices = STAFF_TYPE)  
  institute = models.CharField('Instituto', max_length=40, blank=True, default='instituto') 
  email = models.EmailField('Email', blank=True)
  nickname = models.CharField('Apelido',max_length=40, blank=True)
  projeto = models.CharField('Projeto',max_length=40, blank=True)
  question_answer = models.ManyToManyField(
    Question,   
    through='Answer',
    through_fields=('user', 'question'),
    related_name='question_answer',
  )
  topic_answer = models.ManyToManyField(
    Topic,
    through='TopicAnswer',
    through_fields=('user', 'topic'),
    related_name='topic_answer',
  )


  class Meta:
    verbose_name = 'usuário'
    verbose_name_plural = 'usuários'

  def save(self, *args, **kwargs):
      super(User, self).save(*args, **kwargs)      
      try:
         Termo.objects.get(user=self)
      except:
         Termo.objects.create(user=self)     
         return super(User, self).save(*args, **kwargs)
      return super(User, self).save(*args, **kwargs)


class TopicAnswer(models.Model):        
  user = models.ForeignKey(User)
  topic = models.ForeignKey(Topic)
  text = RichTextUploadingField(config_name='full', verbose_name='')
  answer_date = models.DateTimeField(editable=False)

  def __str__(self):
    return self.text

  def save(self, *args, **kwargs):
    if not self.id:
      self.answer_date = timezone.now()
    return super(TopicAnswer, self).save(*args, **kwargs)

  class Meta:
    verbose_name = 'comentario'
    verbose_name_plural = 'comentarios'


class TopicAnswerForm(forms.ModelForm):
  class Meta:
    model = TopicAnswer
    fields = ['text']


class Answer(models.Model):
  user = models.ForeignKey(User, related_name='user_answer')
  question = models.ForeignKey('Question',related_name='question')
  choice = models.ForeignKey('Choice', related_name='choice', blank=True, null=True)
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

  def user_inst(self):
    return self.user.institute
  user_inst.short_description = 'Instituto'

  def user_stf(self):
    return self.user.get_staff_display()
  user_stf.short_description = 'Staff'

  def userd(self):
    return self.user
  userd.short_description = 'Usuario'

  class Meta:
    verbose_name = 'resposta'
    verbose_name_plural = 'respostas'


class Termo(models.Model):
    user = models.ForeignKey(User, related_name='user_termo')
    condition = models.CharField('Condição', max_length=10, default='Nao')

    def __str__(self):
        return self.condition

    def userd(self):
        return self.user.user

class MeuEspaco(models.Model):
    projeto = models.CharField('Projeto',max_length=100, blank=False)
    user = models.CharField('Usuario',max_length=200, blank=True)
    categoria = models.CharField('Categoria',max_length=50, blank=True)
    publ_date = models.DateTimeField('Data de publicação')
    link =  models.URLField(max_length=1000, blank=True)
    comentario =  models.CharField('Comentário',max_length=1000, blank=True)
    secao = models.CharField('Seção',max_length=30, blank=True)
    arquivo = models.FileField (upload_to = settings.MEDIA_ROOT, max_length=2000000, blank=True)


####### VEIO DA AGORA ########################################################################################3


#projeto-foregnkey
class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)

  def __str__(self):
    return self.choice_text.encode('utf8')

  class Meta:
    verbose_name = 'escolha'
    verbose_name_plural = 'escolhas'


#################### FIM AGORA ########################################################################

################ VINDO DO CONHEÇA #########################

class Article(models.Model):
        
    projeto = models.ForeignKey('Projeto')
    title = models.CharField('Título do artigo',max_length=200)
    tags = TaggableManager()
    article = RichTextUploadingField(config_name='default', verbose_name=u'Descrição')
    publ_date = models.DateTimeField('Data de publicação')
    destaque = models.CharField('Destacado?',max_length=3, default='Não')  
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

  
  ############ FIM CONHECA #######################

  ############ VINDO DO PROJETOS #############



   ################### FIM PROJETOS ###################################
  ### VINDO DE RELATORIO ###########3
class Relatorio(models.Model):
        
    TIPOS = (
        ('1', 'Geral'),
        ('2', 'Questão'),
    )
    projeto = models.ForeignKey('Projeto')
    questao = models.ForeignKey(Question,blank=True, null=True)
    tags = TaggableManager()
    tipo = destaque = models.CharField(max_length=10, choices=TIPOS, default='1')
    titulo =  models.CharField(max_length=100)
    conteudo = RichTextUploadingField(config_name='full', verbose_name=u'Resultado e Análise')
    publ_date = models.DateTimeField(null=True)
    destaque = models.CharField(max_length=3, default='Não')
    address = models.CharField(max_length=200)
    published = models.CharField(max_length=3, default='Não')
    publhistorico = models.CharField(max_length=3, default='Não')
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __int__(self):
        return self.questao.id

    def save(self, *args, **kwargs):
        super(Relatorio, self).save(*args, **kwargs)
        self.address = "{SITE_URL}agora/resultados/relatorio/{id}".format(id=self.id, SITE_URL=settings.SITE_URL)
        return super(Relatorio, self).save(*args, **kwargs)

        ############################# FIM RELATORIO ####################