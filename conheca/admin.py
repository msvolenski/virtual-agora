from django.contrib import admin
from .models import Link, Article, Topic
# Register your models here.


class LinkInline(admin.TabularInline):
    model = Link
    extra = 3


class TopicAdmin(admin.ModelAdmin):
    
    #list_filter = ['pub_date']    
    
    #setam os campos que irão aparecer no "Add adiciona Link"    
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Sessão:', {'fields': ['session']}),         
        #('Data de publicação', {'fields': ['pub_date']}),
           
    ]
   
    inlines = [LinkInline]
    list_display = ['title']
    search_fields = ['title']


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
        ('URL da página do Artigo:', {'fields': ['address']}),   
    ]
   
    
    list_display = ('title', 'id', 'subtitle' , 'article','questao_associada', 'reference','destaque')   
     
    
    def destacar_artigo(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request, "Não é possível destacar mais de um artigo por vez.")
            return         
        else:
            Article.objects.all().update(destaque = 'Não')            
            queryset.update(destaque = 'Sim')
            
            return 
    
    
    
    
    
    
    #search_fields = ['titulo']    
    
admin.site.register(Topic, TopicAdmin )
admin.site.register(Article, ArticleAdmin )