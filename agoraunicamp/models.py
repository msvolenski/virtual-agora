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


class Publicacao(models.Model):
    PUBLICADO = (
      ('sim', 'sim'),
      ('nao', 'nao'),
    )

    ETAPA = (
      ('1', '1'),
      ('2', '2'),
      ('3', '3'),
      ('4', '4'),
      ('5', '5'),
      
    )
    
    
    projeto = models.ForeignKey('Projeto')
    publ_date = models.DateTimeField('Data de publicação', blank=True)
    tags = TaggableManager()
    published = models.CharField('Publicar imediatamente?',max_length=3, choices = PUBLICADO, default='nao')
    etapa_publ = models.CharField("Etapa que será publicado", choices = ETAPA, max_length=1, default='1')
    address = models.CharField('Endereço',max_length=200, default='Preenchimento automatico')


class Projeto(models.Model):
    ETAPA = (
      ('1', '1'),
      ('2', '2'),
      ('3', '3'),
      ('4', '4'),
      ('5', '5'),      
    )

    projeto = models.CharField('Projeto',max_length=100,blank=True, null=True)
    sigla = models.CharField('Sigla', max_length=50, blank=True, null=True)
    etapa_prj = models.CharField("Etapa", choices = ETAPA, max_length=1, default='1')

    def save(self, *args, **kwargs):
      super(Projeto, self).save(*args, **kwargs)      
      cont = 1
      for cont in range(1,6):
        Etapa.objects.get_or_create(project=self, etapa=str(cont))          
      return super(Projeto, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.projeto.encode('utf8')


class Topic(Publicacao):
  title = models.CharField('Título', max_length=50)
  text = RichTextUploadingField(config_name='default', verbose_name=u'Texto')

  def __str__(self):
    return self.title.encode('utf8')

  def save(self, *args, **kwargs):
    super(Topic, self).save(*args, **kwargs)
    self.address = "{SITE_URL}agora/debate/{id}".format(id=self.id, SITE_URL=settings.SITE_URL)
    return super(Topic, self).save(*args, **kwargs)  
  
  class Meta:
    verbose_name = 'debate'
    verbose_name_plural = 'debates'


class Question(Publicacao):
    STATUS_CHOICES = (
        ('nao', 'Não publicado'), # unpublished
        ('sim', 'Publicado'),     # published
    )   

    QUESTION_TYPE = (
        ('1', 'One choice'),
        ('2', 'Multipla Escolha'),
        ('3', 'Texto'),
        ('4', 'Popostas'),
    )
  
    question_type = models.CharField('Tipo', max_length=1, choices = QUESTION_TYPE)
    question_text = models.CharField('Título da Questão',max_length=200)   
    exp_date = models.DateTimeField('Data de expiração')  
    image = models.ImageField('Imagem', upload_to='question_images', blank=True, null=True)

      
    
    def __str__(self):
        nome = str(self.pk) + ' - ' + self.question_text 
        return nome.encode('utf8')

    def save(self, *args, **kwargs):
        super(Question, self).save(*args, **kwargs)
        self.address = "{SITE_URL}agora/participe/{id}".format(id=self.id,SITE_URL=settings.SITE_URL)
        return super(Question, self).save(*args, **kwargs)

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

  avatar = models.ImageField(
      upload_to = 'agoraunicamp/media/img/',
      default = 'agoraunicamp/media/img/no-avatar.jpg',
  )

  primeiro_nome =  models.CharField('Primeiro nome', max_length=40, blank=True)
  ultimo_nome = models.CharField('Sobrenome', max_length=100, blank=True)
  nome_completo = models.CharField('Nome Completo', max_length=200, blank=True)
  staff = models.CharField('Staff', max_length=1, blank=True, choices = STAFF_TYPE)  
  institute = models.CharField('Instituto', max_length=40, blank=True, default='instituto') 
  email = models.EmailField('Email', blank=True)
  nickname = models.CharField('Apelido',max_length=40, blank=True)
  projeto = models.ForeignKey('Projeto', blank=True, null=True)
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
      self.nome_completo = self.primeiro_nome + ' ' + self.ultimo_nome
      try:
         Termo.objects.get(user=self)
      except:
         Termo.objects.create(user=self)     
         return super(User, self).save(*args, **kwargs)
      return super(User, self).save(*args, **kwargs)

  def __str__(self):
    return self.nome_completo


class TopicAnswer(models.Model):        
  user = models.ForeignKey(
      User,
      on_delete = models.CASCADE,
      related_name='topicanswer',
  )
  topic = models.ForeignKey(
      Topic,
      on_delete = models.CASCADE,
      related_name = 'topicanswer',)
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

class TopicAnswerReply(models.Model):        
  user = models.ForeignKey(
      User,
      on_delete = models.CASCADE,
      related_name='topicanswerreply',
  )
  comment = models.ForeignKey(
      TopicAnswer,
      on_delete = models.CASCADE,
      related_name='topicanswerreply',
  )
  text = RichTextUploadingField(config_name='full', verbose_name='')
  answer_date = models.DateTimeField(editable=False)

  def __str__(self):
    return self.text

  def save(self, *args, **kwargs):
    if not self.id:
      self.answer_date = timezone.now()
    return super(TopicAnswerReply, self).save(*args, **kwargs)

  class Meta:
    verbose_name = 'Réplica'
    verbose_name_plural = 'Réplicas'


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
        return self.user


class MeuEspaco(models.Model):
    projeto = models.CharField('Projeto',max_length=100, blank=False)
    user = models.CharField('Usuario',max_length=200, blank=True)
    categoria = models.CharField('Categoria',max_length=50, blank=True, null=True)
    publ_date = models.DateTimeField('Data de publicação')
    link =  models.URLField(max_length=1000, blank=True, null=True)
    comentario =  models.CharField('Comentário',max_length=1000)
    secao = models.CharField('Seção',max_length=30, blank=True, null=True)
    arquivo = models.FileField(upload_to=settings.MEDIA_ROOT, max_length=2000000, blank=True, null=True)
    


class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)

  def __str__(self):
    return self.choice_text.encode('utf8')

  class Meta:
    verbose_name = 'escolha'
    verbose_name_plural = 'escolhas'


class Article(Publicacao):    
    title = models.CharField('Título do artigo', max_length=200)    
    text = RichTextUploadingField(config_name='default', verbose_name=u'Descrição')
    
    def __str__(self):
        return self.title.encode('utf8')

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        self.address = "{SITE_URL}agora/conheca/artigos/{id}".format(id=self.id, SITE_URL=settings.SITE_URL)
        return super(Article, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'


class Relatorio(Publicacao):        

    
    TIPOS = (
        ('1', 'Resultado Geral (não associado a alguma questão)'),
        ('2', 'Resultado Específico (assciado a uma questão)'),
    )

    TIPOS_G = (
        ('0', 'Sem Gráfico ou Tabela'),
        ('1', 'Gráfico de  Barras'),
        ('2', 'Gráfico de Pizza'),
        ('3', 'Tabela de Propostas'),
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
      ('9', 'todos')
    )

    PROPOSTA_ORG = (
      ('0', 'Não é resultado do tipo Propostas'),
      ('1', 'Da Questão Associada (certifique-se que a Questão é do tipo "Propostas"'),
      ('2', 'Do Campo "PROPOSTAS" abaixo'),
    )

    questao = models.ForeignKey(Question, blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=TIPOS, default='0')
    titulo =  models.CharField(max_length=100)
    conteudo = RichTextUploadingField(config_name='full', verbose_name=u'Resultado e Análise')
    grafico = models.CharField(max_length=10, choices=TIPOS_G, default='1')
    filtro_staff = models.CharField(max_length=3, choices=STAFF_TYPE, default='9')
    arquivo = models.CharField(max_length=200, default='null')
    propostas_org =  models.CharField('Origem', max_length=3, choices=PROPOSTA_ORG, default='0')
   
    def __int__(self):
      return self.questao.pk
    
    def __str__(self):
      if self.questao is None:      
        return 'Relatorio Geral (n. ' + str(self.pk) + ')'
      else:
        return 'Relatorio (n. ' + str(self.id) + '): Questao -  ' + str(self.questao.pk)      
       
       
    def save(self, *args, **kwargs):
        super(Relatorio, self).save(*args, **kwargs)
        self.address = "{SITE_URL}agora/resultados/relatorio/{id}".format(id=self.id, SITE_URL=settings.SITE_URL)
        return super(Relatorio, self).save(*args, **kwargs)


class Etapa(models.Model):
    project = models.ForeignKey(Projeto, on_delete=models.CASCADE, verbose_name='Projeto')
    etapa = models.CharField("Etapa", max_length=1, default='1')
    name = models.CharField("Nome da etapa", max_length=100, default='Ideias')
    header_txt = models.TextField("Cabeçalho", default='null')
    objetivo_txt = models.TextField("Objetivo", default='null')
    participar_txt = models.TextField("Como participar", default='null')
    resultado_txt = models.TextField("Resultado", default='null')
    termino = models.TextField("Termino", default='null')

class Proposta(models.Model):
    relatorio = models.ForeignKey(
      Relatorio,
      on_delete=models.CASCADE,
      related_name = 'proposta',  
    )
    proposta_text = models.TextField('Proposta')
    ranking = models.CharField("Ranking", max_length=5, default='1')
    indice = models.IntegerField("Indice", default=1000)
    curtidas = models.IntegerField("Curtidas", default=0)
    naocurtidas = models.IntegerField("Não Curtidas", default=0)
    
    def __str__(self):
      return self.proposta_text.encode('utf8')

    class Meta:
      verbose_name = 'proposta'
      verbose_name_plural = 'propostas'

class Curtir(models.Model):
    proposta = models.ForeignKey(
      Proposta,
      on_delete=models.CASCADE,
      related_name = 'curtir',  
    )
    user = models.ForeignKey(
      User,
      on_delete = models.CASCADE,
      related_name='curtir',
    )
    tipo = models.CharField("Curtir/Não Curtir", max_length=10)

        


# class Projeto(models.Model):
#     projeto = models.CharField('Projeto',max_length=100,blank=True, null=True)
#     sigla = models.CharField('Sigla', max_length=50, blank=True, null=True)
#     etapa_prj = models.CharField("Etapa", max_length=1, default='1')

#     def __str__(self):
#         return '%s %s' % (self.sigla, self.projeto)


# class Topic(models.Model):
#   title = models.CharField('Título', max_length=50)
#   text = RichTextUploadingField(config_name='default', verbose_name=u'Texto')
#   publ_date = models.DateTimeField('Data de publicação')
#   tags = TaggableManager()
#   published = models.CharField('Publicado?',max_length=3, default='nao')
#   projeto = models.ForeignKey('Projeto', max_length=50, blank=False)
#   address = models.CharField('Endereço',max_length=200)

#   def __str__(self):
#     return self.title.encode('utf8')

#   class Meta:
#     verbose_name = 'debate'
#     verbose_name_plural = 'debates'


# class Question(models.Model):
#     STATUS_CHOICES = (
#         ('nao', 'Não publicado'), # unpublished
#         ('sim', 'Publicado'),     # published
#     )   

#     QUESTION_TYPE = (
#         ('1', 'One choice'),
#         ('2', 'Multipla Escolha'),
#         ('3', 'Texto'),
#     )

#     projeto = models.ForeignKey('Projeto')
#     question_type = models.CharField('Tipo', max_length=1, choices = QUESTION_TYPE)
#     question_text = models.CharField('Título da Questão',max_length=200)
#     publ_date = models.DateTimeField('Data de publicação')
#     exp_date = models.DateTimeField('Data de expiração')
#     published = models.CharField('Publicado?',max_length=3, default='nao')
#     image = models.ImageField('Imagem', upload_to='question_images', blank=True, null=True)
#     tags = TaggableManager()
#     address = models.CharField('Endereço',max_length=200)

#     def __str__(self):
#         return self.question_text.encode('utf8')

#     def save(self, *args, **kwargs):
#         super(Question, self).save(*args, **kwargs)
#         self.address = "{SITE_URL}agora/participe/{id}".format(id=self.id,SITE_URL=settings.SITE_URL)
#         return super(Question, self).save(*args, **kwargs)

#     class Meta:
#         verbose_name = 'questão'
#         verbose_name_plural = 'questões'


# class User(models.Model):
#   user = models.OneToOneField(
#     AuthUser,
#     primary_key=True,
#     parent_link=True, 
#   )

#   STAFF_TYPE = (
#       ('1', 'Professor'),
#       ('2', 'Funcionario'),
#       ('3', 'Aluno-Graduacao'),
#       ('4', 'Aluno-Mestrado'),
#       ('5', 'Aluno-Doutorado'),
#       ('6', 'Aluno-Especial'),
#       ('7', 'Aluno-Lato'),
#       ('8', 'outro'),
#   )

#   primeiro_nome =  models.CharField('Primeiro nome', max_length=40, blank=True)
#   ultimo_nome =  models.CharField('Sobrenome', max_length=100, blank=True)
#   staff = models.CharField('Staff', max_length=1, blank=True, choices = STAFF_TYPE)  
#   institute = models.CharField('Instituto', max_length=40, blank=True, default='instituto') 
#   email = models.EmailField('Email', blank=True)
#   nickname = models.CharField('Apelido',max_length=40, blank=True)
#   projeto = models.CharField('Projeto',max_length=40, blank=True)
#   question_answer = models.ManyToManyField(
#     Question,   
#     through='Answer',
#     through_fields=('user', 'question'),
#     related_name='question_answer',
#   )
#   topic_answer = models.ManyToManyField(
#     Topic,
#     through='TopicAnswer',
#     through_fields=('user', 'topic'),
#     related_name='topic_answer',
#   )

#   class Meta:
#     verbose_name = 'usuário'
#     verbose_name_plural = 'usuários'

#   def save(self, *args, **kwargs):
#       super(User, self).save(*args, **kwargs)      
#       try:
#          Termo.objects.get(user=self)
#       except:
#          Termo.objects.create(user=self)     
#          return super(User, self).save(*args, **kwargs)
#       return super(User, self).save(*args, **kwargs)


# class TopicAnswer(models.Model):        
#   user = models.ForeignKey(User)
#   topic = models.ForeignKey(Topic)
#   text = RichTextUploadingField(config_name='full', verbose_name='')
#   answer_date = models.DateTimeField(editable=False)

#   def __str__(self):
#     return self.text

#   def save(self, *args, **kwargs):
#     if not self.id:
#       self.answer_date = timezone.now()
#     return super(TopicAnswer, self).save(*args, **kwargs)

#   class Meta:
#     verbose_name = 'comentario'
#     verbose_name_plural = 'comentarios'


# class TopicAnswerForm(forms.ModelForm):
#   class Meta:
#     model = TopicAnswer
#     fields = ['text']


# class Answer(models.Model):
#   user = models.ForeignKey(User, related_name='user_answer')
#   question = models.ForeignKey('Question',related_name='question')
#   choice = models.ForeignKey('Choice', related_name='choice', blank=True, null=True)
#   text = models.TextField(max_length=200, blank=True, null=True)
#   answer_date = models.DateTimeField(editable=False)

#   def __str__(self):
#     if self.choice:
#       return self.choice.choice_text
#     return self.text

#   def save(self, *args, **kwargs):
#     if not self.id:
#       self.answer_date = timezone.now()
#     return super(Answer, self).save(*args, **kwargs)

#   def user_inst(self):
#     return self.user.institute
#   user_inst.short_description = 'Instituto'

#   def user_stf(self):
#     return self.user.get_staff_display()
#   user_stf.short_description = 'Staff'

#   def userd(self):
#     return self.user
#   userd.short_description = 'Usuario'

#   class Meta:
#     verbose_name = 'resposta'
#     verbose_name_plural = 'respostas'


# class Termo(models.Model):
#     user = models.ForeignKey(User, related_name='user_termo')
#     condition = models.CharField('Condição', max_length=10, default='Nao')

#     def __str__(self):
#         return self.condition

#     def userd(self):
#         return self.user.user


# class MeuEspaco(models.Model):
#     projeto = models.CharField('Projeto',max_length=100, blank=False)
#     user = models.CharField('Usuario',max_length=200, blank=True)
#     categoria = models.CharField('Categoria',max_length=50, blank=True)
#     publ_date = models.DateTimeField('Data de publicação')
#     link =  models.URLField(max_length=1000, blank=True)
#     comentario =  models.CharField('Comentário',max_length=1000, blank=True)
#     secao = models.CharField('Seção',max_length=30, blank=True)
#     arquivo = models.FileField (upload_to = settings.MEDIA_ROOT, max_length=2000000, blank=True)


# class Choice(models.Model):
#   question = models.ForeignKey(Question, on_delete=models.CASCADE)
#   choice_text = models.CharField(max_length=200)

#   def __str__(self):
#     return self.choice_text.encode('utf8')

#   class Meta:
#     verbose_name = 'escolha'
#     verbose_name_plural = 'escolhas'


# class Article(models.Model):        
#     projeto = models.ForeignKey('Projeto')
#     title = models.CharField('Título do artigo',max_length=200)
#     tags = TaggableManager()
#     article = RichTextUploadingField(config_name='default', verbose_name=u'Descrição')
#     publ_date = models.DateTimeField('Data de publicação') 
#     address = models.CharField('Endereço',max_length=200)
#     published = models.CharField('Publicado?',max_length=3, default='nao')

#     def __str__(self):
#         return self.title.encode('utf8')

#     def save(self, *args, **kwargs):
#         super(Article, self).save(*args, **kwargs)
#         self.address = "{SITE_URL}agora/conheca/artigos/{id}".format(id=self.id, SITE_URL=settings.SITE_URL)
#         return super(Article, self).save(*args, **kwargs)

#     class Meta:
#         verbose_name = 'Artigo'
#         verbose_name_plural = 'Artigos'


# class Relatorio(models.Model):
        
#     TIPOS = (
#         ('1', 'Geral'),
#         ('2', 'Questão'),
#     )
#     projeto = models.ForeignKey('Projeto')
#     questao = models.ForeignKey(Question,blank=True, null=True)
#     tags = TaggableManager()
#     tipo = models.CharField(max_length=10, choices=TIPOS, default='1')
#     titulo =  models.CharField(max_length=100)
#     conteudo = RichTextUploadingField(config_name='full', verbose_name=u'Resultado e Análise')
#     publ_date = models.DateTimeField(null=True)
#     address = models.CharField(max_length=200)
#     published = models.CharField(max_length=3, default='nao')

#     def __int__(self):
#         return self.questao.id

#     def save(self, *args, **kwargs):
#         super(Relatorio, self).save(*args, **kwargs)
#         self.address = "{SITE_URL}agora/resultados/relatorio/{id}".format(id=self.id, SITE_URL=settings.SITE_URL)
#         return super(Relatorio, self).save(*args, **kwargs)


# class Etapa(models.Model):
#     project = models.ForeignKey(Projeto, on_delete=models.CASCADE, verbose_name='Projeto')
#     etapa = models.CharField("Etapa", max_length=1, default='1')
#     name = models.CharField("Nome da etapa", max_length=100, default='Ideias')
#     header_txt = models.TextField("Cabeçalho", default='null')
#     objetivo_txt = models.TextField("Objetivo", default='null')
#     participar_txt = models.TextField("Como participar", default='null')
#     resultado_txt = models.TextField("Resultado", default='null')