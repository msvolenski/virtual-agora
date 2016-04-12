# -*- coding: utf-8 -*-
from datetime import timedelta
from django.contrib.auth.models import User as AuthUser
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from forum.models import User as Userf
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from agoraunicamp.models import User, Message, Projeto

#projeto
def getProject():
    try:
        choices =[ (o.sigla, o.sigla) for o in Projeto.objects.all()]
    except:
        choices = [("Default", "Default")]
    return choices

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

    projeto = models.CharField('Projeto', max_length=50, blank=False, choices = getProject())
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
            return "#{id} - {question}".format(id=self.id, question=self.question_text)
        else:
            return self.question_text

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

#projeto-foregnkey
class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)

  def __str__(self):
    return self.choice_text

  class Meta:
    verbose_name = 'escolha'
    verbose_name_plural = 'escolhas'

class InitialListQuestion(models.Model):
    projeto = models.CharField('Projeto', max_length=50, blank=False, choices = getProject())
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
