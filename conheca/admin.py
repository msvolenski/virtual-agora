from django.contrib import admin
from .models import Link, Article, Topic
from django.utils import timezone
# Register your models here.


class LinkInline(admin.TabularInline):
    model = Link
    extra = 3


class TopicAdmin(admin.ModelAdmin):
    
    list_filter = ['session']    
    actions = ['inverter_ordem_de_apresentacao']
    #setam os campos que irão aparecer no "Add adiciona Link"    
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Sessão:', {'fields': ['session']}),  
        
        #('Data de publicação', {'fields': ['pub_date']}),
           
    ]
   
    inlines = [LinkInline]
    list_display = ('title','id','position','session')
    search_fields = ['title']
    
    def inverter_ordem_de_apresentacao(modeladmin, request, queryset):             
            if queryset.count() > 2:
                modeladmin.message_user(request, "Só é possível inverter dois tópicos por vez.")
                return         
            else:                        
                a = queryset.first()
                a1 = a.position                                
                b = queryset.last()
                b1 = b.position                 
                queryset.filter(id=a.pk).update(position = b1)               
                queryset.filter(id=b.pk).update(position = a1)
               
                
            return

class ArticleAdmin(admin.ModelAdmin):
    
    list_filter = ['tags']    
    actions = ['destacar_artigo','publicar_na_pagina_principal','desfazer_publicacao_na_pagina_principal'] 
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Sub-título', {'fields': ['subtitle']}),         
        ('Conteúdo', {'fields': ['article']}),
        ('Tags', {'fields': ['tags']}), 
        ('Questões associada a este Artigo', {'fields': ['questao_associada']}),          
        ('Data de Pubicação:', {'fields': ['publ_date']}), 
        ('URL da página do Artigo:', {'fields': ['address']}),   
    ]
   
    
    list_display = ('title', 'id', 'publ_date', 'subtitle' , 'article','questao_associada', 'published','destaque')   
     
    
    def destacar_artigo(modeladmin, request, queryset):
        if queryset.count() != 1:
            modeladmin.message_user(request, "Não é possível destacar mais de um artigo por vez.")
            return         
        else:
            Article.objects.all().update(destaque = 'Não')            
            queryset.update(destaque = 'Sim')
            
            return
            
    def publicar_na_pagina_principal(modeladmin, request, queryset):             
            queryset.update(published = 'Sim')
            queryset.update(publ_date = timezone.now())           
            return 
    
    def desfazer_publicacao_na_pagina_principal(modeladmin, request, queryset):             
            queryset.update(published = 'Não')
            return 
    
    
    
    
    #search_fields = ['titulo']    
    
admin.site.register(Topic, TopicAdmin )
admin.site.register(Article, ArticleAdmin )