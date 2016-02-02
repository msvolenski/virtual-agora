from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
# Create your models here.



    
        
class Article(models.Model):
    
    def get_address():
        try:
            art = Article.objects.latest('id') 
        except (KeyError, Article.DoesNotExist):
            return str('http://127.0.0.1:8000/agora/pdpu/conheca/artigos/') + str(1)            
        a = art.pk
        a = a + 1        
        return str('http://127.0.0.1:8000/agora/pdpu/conheca/artigos/') + str(a)     
        #return 'http://127.0.0.1:8000/agora/pdpu/conheca/artigos/7/' (page)   
    

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    tags = TaggableManager()
    article = models.TextField()
    publ_date = models.DateTimeField()
    destaque = models.CharField(max_length=3, default='Não')    
    questao_associada = models.CommaSeparatedIntegerField(max_length=100, blank=True)  
    address = models.CharField(max_length=200, default=get_address)
    published = models.CharField(max_length=3, default='Não')     
    
    def __str__(self):
        return self.title
        
    def split_numbers(self):
        return self.questao_associada.split(',')
        

        
        
class Topic(models.Model):    
    SESSION_TYPE = (
    ('1', 'Sobre o PDPU'),
    ('2', 'Outras informações'),
)    
    

    def get1_pk1():
        try:
            t = Topic.objects.latest('id')
        except (KeyError, Topic.DoesNotExist):
            return 1
        a = t.pk
        a = a + 1     
        return a
    
    title = models.CharField(max_length=200)
    session = models.CharField(max_length=1, choices = SESSION_TYPE)
    position = models.CharField(max_length=200, default=get1_pk1)

    def __str__(self):
        return self.title
 

       
class Link(models.Model):

    title = models.ForeignKey(Topic, on_delete=models.CASCADE)
    url = models.URLField(max_length=1000)
    url_title = models.CharField(max_length=1000)
    

    def __str__(self):
        return self.url        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        