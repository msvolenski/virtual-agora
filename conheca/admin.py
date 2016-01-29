from django.contrib import admin
from .models import AdicionaLink, Article
# Register your models here.

class AdicionaLinknAdmin(admin.ModelAdmin):
    
    list_filter = ['data_publicacao']    
    
    #setam os campos que irão aparecer no "Add adiciona Link"    
    fieldsets = [
        (None,               {'fields': ['titulo']}),
        ('URL:', {'fields': ['url']}),         
        ('Data de publicação', {'fields': ['data_publicacao']}),
           
    ]
   
    
    list_display = ('titulo', 'url' , 'data_publicacao' )
    search_fields = ['titulo']
    

class ArticleAdmin(admin.ModelAdmin):
    
    #list_filter = ['data_publicacao']    
    actions = ['destacar_artigo'] 
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Sub-título', {'fields': ['subtitle']}),         
        ('Conteúdo', {'fields': ['article']}),
        ('Tags', {'fields': ['tags']}), 
        ('Questões associada a este Artigo', {'fields': ['questao_associada']}),          
        ('Referências', {'fields': ['reference']}),          
    ]
   
    
    list_display = ('title', 'subtitle' , 'article','questao_associada', 'reference','destaque')   
    
    
    def destacar_artigo(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request, "Não é possível destacar mais de um artigo por vez.")
            return         
        else:
            Article.objects.all().update(destaque = 'Não')            
            queryset.update(destaque = 'Sim')
            
            return 
    
    
    
    
    
    
    #search_fields = ['titulo']    
    
admin.site.register(AdicionaLink, AdicionaLinknAdmin )
admin.site.register(Article, ArticleAdmin )