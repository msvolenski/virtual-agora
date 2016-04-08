# -*- coding: utf-8 -*-
from datetime import timedelta
from django.contrib.auth.models import User as AuthUser
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from forum.models import User as Userf
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from agoraunicamp.models import User



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

    question_type = models.CharField('Tipo', max_length=1, choices = QUESTION_TYPE)
    question_text = models.CharField('Título da Questão',max_length=200)
    publ_date = models.DateTimeField('Data de publicação')
    exp_date = models.DateTimeField('Data de expiração')
    days = models.IntegerField('Tempo para expirar', choices=EXP_TIME, default=3650)
    question_status = models.CharField('Estado da questão', max_length=1, choices=STATUS_CHOICES, default = 'p')
    answer_status = models.CharField('Estado da resposta', max_length=1, choices=STATUS_CHOICES, default = 'n')
    image = models.ImageField('Imagem', upload_to='question_images', blank=True, null=True)
    tags = TaggableManager()
    address = models.CharField('Endereço',max_length=200)
    permissao = models.IntegerField(default=0)
    resultado = models.CharField(max_length=1, choices=STATUS_CHOICES , default = 'n')


    def __str__(self):
        if self.id:
            return "#{id} - {question}".format(id=self.id, question=self.question_text)
        else:
            return self.question_text

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.publ_date = timezone.now()
        self.update_expiration_time()
        super(Question, self).save(*args, **kwargs)
        self.address = "{SITE_URL}agora/pdpu/participe/{id}".format(id=self.id,SITE_URL=settings.SITE_URL)
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


class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)

  def __str__(self):
    return self.choice_text

  class Meta:
    verbose_name = 'escolha'
    verbose_name_plural = 'escolhas'


# class User(models.Model):
#   user = models.OneToOneField(
#     AuthUser,
#     primary_key=True,
#     parent_link=True,
#   )
#
#   STAFF_TYPE = (
#       ('1', 'Professor'),
#       ('2', 'Funcionário'),
#       ('3', 'Aluno'),
#       ('4', 'Outro'),
#   )
#
#   primeiro_nome =  models.CharField('Primeiro nome', max_length=40, blank=True)
#   ultimo_nome =  models.CharField('Sobrenome', max_length=100, blank=True)
#   staff = models.CharField('Staff', max_length=1, blank=True, choices = STAFF_TYPE)
#   year_of_start = models.IntegerField('Ano de ingresso',blank=True, default='9999')
#   course = models.CharField('Curso', max_length=40, blank=True , default='curso')
#   institute = models.CharField('Instituto', max_length=40, blank=True, default='instituto')
#   academic_registry = models.IntegerField('Registro acadêmico',default='9999')
#   email = models.EmailField('Email', blank=True)
#   nickname = models.CharField('Apelido',max_length=40, blank=True)
#   question_answer = models.ManyToManyField(
#     Question,
#     through='Answer',
#     through_fields=('user', 'question'),
#     related_name='question_answer',
#   )
#
#   class Meta:
#     verbose_name = 'usuário'
#     verbose_name_plural = 'usuários'
#
#   def save(self, *args, **kwargs):
#       super(User, self).save(*args, **kwargs)
#       nome = self.user.user
#       try:
#          Termo.objects.get(user=nome)
#       except:
#          Termo.objects.create(user=self)
#          Userf.objects.create(user=self.user)
#          a = Userf.objects.get(user=self.user)
#          a.username="{A} {B}".format(A=self.primeiro_nome,B=self.ultimo_nome)
#          a.save()
#          return super(User, self).save(*args, **kwargs)
#       return super(User, self).save(*args, **kwargs)



class InitialListQuestion(models.Model):
    name = models.CharField('Nome da lista', max_length=50)
    questions = TaggableManager('Questões')
    select = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.select

    def is_list_active(self):
        if self.select == 1:
            return True
        else:
            return False

    def split_questions(self):
        return self.questions.split(',')

    is_list_active.boolean = True
    is_list_active.short_description = 'Lista ativa?'

    class Meta:
        verbose_name = 'Lista de Questões para o Home'
        verbose_name_plural = 'Lista de Questões para o Home'

class Message(models.Model):
        MESSAGE_TYPE = (
            ('1', 'Conheça'),
            ('2', 'Resultados'),
            ('3', 'Comunidade'),
            ('4', 'Participe'),
        )
        published = models.CharField('Publicado?',max_length=3, default='Não')
        kind = models.CharField('Tipo', max_length=1, choices = MESSAGE_TYPE)
        publ_date = models.DateTimeField('Data de publicação')
        message = models.CharField('Recado', max_length=500)
        address = models.CharField('Endereço',max_length=200, blank=True)



class MeuEspacoArtigo(models.Model):

    user = models.CharField('Usuario',max_length=200, blank=True)
    categoria = models.CharField('Categoria',max_length=20, blank=True)
    publ_date = models.DateTimeField('Data de publicação')
    link =  models.URLField(max_length=1000, blank=True)
    comentario =  models.CharField('Comentário',max_length=200, blank=True)
    secao = models.CharField('Seção',max_length=30, blank=True)
    arquivo = models.FileField (upload_to = settings.MEDIA_ROOT, max_length=2000000, blank=True)
