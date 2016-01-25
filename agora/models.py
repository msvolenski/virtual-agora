import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django import forms
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.forms import CheckboxSelectMultiple
from django.shortcuts import get_object_or_404, render
# Create your models here.
#Chama a classe "models"

STATUS_CHOICES = (
    ('n', 'Não publicado'),
    ('p', 'Publicado'),
    
)

#==============================================================================
# Classe que insere novos atributos para a Classe User
#==============================================================================
@python_2_unicode_compatible
class UserProfile(models.Model):
   # This field is required.
    user = models.OneToOneField(User)

     #Novos Atributos
    ano_de_ingresso = models.CharField(max_length=20)
    faculdade = models.CharField(max_length=20, default = 'faculdade') 
    curso = models.CharField(max_length=20)
    

#==============================================================================
# As classes abaixo estabelecem uma tabela com o nome do usuário, a questão respondida e o voto 
#==============================================================================
class Usuario(models.Model):
    nome = models.CharField(max_length=200)    

    def __str__(self):              # __unicode__ on Python 2
        return str(self.nome)    

class QuestoesRespondidas(models.Model): 
        
    questao = models.CharField(max_length=200)    
    usuario = models.ManyToManyField(Usuario)
    
    
    def __str__(self):              # __unicode__ on Python 2
        return self.questao  

class VotoDoUsuario(models.Model):
    
    faculdade = models.CharField(max_length=20, null=True)     
    voto = models.CharField(max_length=200) 
    questao = models.CharField(max_length=200) 
    user = models.ForeignKey('Usuario',on_delete=models.CASCADE,)
        
    def __str__(self):              # __unicode__ on Qython 2
        return "%s %s" % (self.voto, self.questao)        
        
#==============================================================================
# OBJETO: QUESTION
# Define "Question", objeto que modela as perguntas
#==============================================================================
@python_2_unicode_compatible  # only if you need to support Python 2
class Question(models.Model):
    QUESTION_TYPE = (
    ('1', 'One choice'),
    ('2', 'Multipla Escolha'),
    ('3', 'Texto'),    
)
    
        
    
    
    
    def define_next():
        try:
            question = Question.objects.latest('id')  
        except (KeyError, Question.DoesNotExist):
            return str('#') + str(1).ljust(3) + str('-').ljust(3)            
           
        a = question.pk
        a = a + 1        
        return str('#') + str(a).ljust(3) + str('-').ljust(3)
      
        
    
    permissao = models.IntegerField(max_length=10, default=0)
    question_text = models.CharField(max_length=200, default=define_next)
    pub_date = models.DateTimeField('date published')
    tags = TaggableManager()
    resultado = models.CharField(max_length=1, choices=STATUS_CHOICES , default = 'n')
    question_type = models.CharField(max_length=1, choices = QUESTION_TYPE) 
    
    def __str__(self):
        return "%s %s" % (self.pk, self.question_text)
        
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'       

#==============================================================================
# OBJETO: Choice
# Define "Choice", objeto que adiciona um campo de multipla escolha para as Perguntas 
#==============================================================================
@python_2_unicode_compatible  # only if you need to support Python 2
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.choice_text

#==============================================================================
# OBJETO: ADCIONALINK
# Define "AdicionaLink", objeto que escreve URLs no campo "Conheça"
#==============================================================================
@python_2_unicode_compatible
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
        






