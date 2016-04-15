from django.contrib import admin
from .models import Projeto
# Register your models here.


class ProjetoAdmin(admin.ModelAdmin):
  #actions = ['show_results']
  list_display = ['projeto', 'sigla']
  #list_filter = ['question', 'choice']


admin.site.register(Projeto, ProjetoAdmin)
