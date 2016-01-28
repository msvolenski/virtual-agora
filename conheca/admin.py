from django.contrib import admin
from .models import AdicionaLink
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
    
    
    
admin.site.register(AdicionaLink, AdicionaLinknAdmin )