from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from agora.models import Question
from smart_selects.db_fields import ChainedForeignKey 
# Create your models here.



    
#        
#class Relatorio_geral(models.Model):
##    
##    def get_address():
##        try:
##            art = Article.objects.latest('id') 
##        except (KeyError, Article.DoesNotExist):
##            return str('http://127.0.0.1:8000/agora/pdpu/conheca/artigos/') + str(1)            
##        a = art.pk
##        a = a + 1        
##        return str('http://127.0.0.1:8000/agora/pdpu/conheca/artigos/') + str(a)     
##        #return 'http://127.0.0.1:8000/agora/pdpu/conheca/artigos/7/' (page)   
##    
##
#    title = models.CharField(max_length=200)#    
#    tags = TaggableManager()
#    conteudo = RichTextUploadingField(config_name='full', verbose_name=u'Descrição')
#    publ_date = models.DateTimeField()
##    destaque = models.CharField(max_length=3, default='Não')    
##    questao_associada = models.CommaSeparatedIntegerField(max_length=100, blank=True)  
#    address = models.CharField(max_length=200, default='1')
#    published = models.CharField(max_length=3, default='Não')     
##    
#    def __str__(self):
#        return self.title
##        
##    def split_numbers(self):
##        return self.questao_associada.split(',')


class Relatorio(models.Model):

    TIPOS = (
        ('1', 'Geral'),
        ('2', 'Questão'),
    )  

#def get_address():
#        try:
#            art = Article.objects.latest('id') 
#        except (KeyError, Article.DoesNotExist):
#            return str('http://127.0.0.1:8000/agora/pdpu/conheca/artigos/') + str(1)            
#        a = art.pk
#        a = a + 1        
#        return str('http://127.0.0.1:8000/agora/pdpu/conheca/artigos/') + str(a)     
#        #return 'http://127.0.0.1:8000/agora/pdpu/conheca/artigos/7/' (page)   
#    
    def get_address():
        try:
            art = Relatorio.objects.latest('id') 
        except (KeyError, Relatorio.DoesNotExist):
            return str('http://127.0.0.1:8000/agora/pdpu/resultados/relatorio/') + str(1)            
        a = art.pk
        a = a + 1        
        return str('http://127.0.0.1:8000/agora/pdpu/resultados/relatorio/') + str(a)     
        #return 'http://127.0.0.1:8000/agora/pdpu/conheca/artigos/7/' (page)   
    
    
    questao = models.ForeignKey(Question,blank=True, null=True)
    #questao =#   Question,
       # chained_field="tipo",
       # chained_model_field="Geral",
       # show_all=False,
       # auto_choose=True
    #)
    tags = TaggableManager()    
    tipo = destaque = models.CharField(max_length=10, choices=TIPOS, default='1')         
    #questao = models.CharField(max_length=200, choices=QUESTOES, default=' ')#    
    titulo =  models.CharField(max_length=100)         
    conteudo = RichTextUploadingField(config_name='full', verbose_name=u'Resultado e Análise')
    publ_date = models.DateTimeField(null=True)
    destaque = models.CharField(max_length=3, default='Não')    
#    questao_associada = models.CommaSeparatedIntegerField(max_length=100, blank=True)  
    address = models.CharField(max_length=200, default=get_address)
    published = models.CharField(max_length=3, default='Não') 
    publhistorico = models.CharField(max_length=3, default='Não')     
#    
    def __int__(self):
        return self.questao.id
#        
#    def split_numbers(self):
#        return self.questao_associada.split(',')







      
#class Topico(models.Model):
#    
#    def get_address_topico():
#        try:
#            tpc = Topico.objects.latest('id') 
#        except (KeyError, Topico.DoesNotExist):
#            return str('http://127.0.0.1:8000/agora/pdpu/conheca/topicos/') + str(1)            
#        a = tpc.pk
#        a = a + 1        
#        return str('http://127.0.0.1:8000/agora/pdpu/conheca/topicos/') + str(a) 
#        
#    def position_det():
#        try:
#            tpc = Topico.objects.latest('position') 
#        except (KeyError, Topico.DoesNotExist):
#            return 1            
#        a = tpc.position
#        a = a + 1        
#        return a
#    
#    
#    
#   topico = models.CharField(max_length=200)
#    address_topico = models.CharField(max_length=200, default=get_address_topico) 
#    position = models.IntegerField(default=position_det)
#    
#    def __str__(self):
#        return self.topico 
#        
#    def __int__(self):
#        return self.position 
#        
#class SubTopico(models.Model):       
#    
#    subtopico = models.ForeignKey(Topico, on_delete=models.CASCADE)
#    subtopico_nome = models.CharField(max_length=200)
#    
#    def __str__(self):
#        return "%s %s" % (self.subtopico, self.subtopico_nome)
#
#class Link(models.Model):
#
#    title = models.ForeignKey(SubTopico, on_delete=models.CASCADE)
#    url = models.URLField(max_length=1000)
#    url_title = models.CharField(max_length=1000)
#    
#    def __str__(self):
#        return self.url        
#        
#        