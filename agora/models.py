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

# Create your models here.
#Chama a classe "models"



#==============================================================================
# Classe que insere novos atributos para a Classe User
#==============================================================================
@python_2_unicode_compatible
class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Novos Atributos
    accepted_eula = models.BooleanField()
    favorite_animal = models.CharField(max_length=20, default="Dragons.")
   

#==============================================================================
# As duas classes abaixos armazenam o nome do usuáio e as questões respondidas por ele    
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


#==============================================================================
# OBJETO: QUESTION
# Define "Question", objeto que modela as perguntas
#==============================================================================
@python_2_unicode_compatible  # only if you need to support Python 2
class Question(models.Model):
        
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    tags = TaggableManager()
    
    def __str__(self):
        return self.question_text
        
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
        






