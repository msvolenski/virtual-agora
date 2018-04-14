from django.contrib import admin
from .models import CorrigePalavra, TextoPreproc,ParametrosDeAjuste, ListaDeSubstantivos, DadosPreproc,TestaPalavra, ListaVertices, TabelaRanking, ListaDeAdjacencias, DadosSelecaoTemas, PesosEAlpha, TemasNew, ProtoFrasesNew, ExtracaoNew, DadosExtracaoNew

# Register your models here.


class TextoPreprocAdmin(admin.ModelAdmin):
  list_display = ['id', 'vertice_num','vertice']

class ListaVerticesAdmin(admin.ModelAdmin):
  list_display = ['id','index', 'node']

class CorrigePalavraAdmin(admin.ModelAdmin):
  list_display = ['palavra','palavra_correta']
  ordering = ['palavra']
  actions = ['delete_selected']

class DadosPreprocAdmin(admin.ModelAdmin):
  list_display = ['flag_completo','flag_testapalavra','corretor','id','palavras_por_sentenca_lssw', 'palavras_por_sentenca_org','quantidade_de_sentencas','palavras_texto_original', 'palavras_texto_lematizado','palavras_texto_lematizado_ssw','nome_rel_protofrase']

class TabelaRankingAdmin(admin.ModelAdmin):
  list_display = ['vertice_nome','vertice_numero','grau', 'grau_norm', 'betweenness','betweenness_norm','eigenvector','eigenvector_norm', 'potenciacao']

class ListaDeAdjacenciasAdmin(admin.ModelAdmin):
  list_display = ['vertice_i','vertice_f','peso']


class DadosSelecaoTemasAdmin(admin.ModelAdmin):
  list_display = ['p_grau','p_bet','p_eigen']

class PesosEAlphaAdmin(admin.ModelAdmin):
  list_display = ['alpha','alphaesp','erro','p_grau','p_betw','p_eigene']

class TemasNewAdmin(admin.ModelAdmin):
  list_display = ['tema','irt','irt_p']

class ListaDeSubstantivosAdmin(admin.ModelAdmin):
  list_display = ['palavra','substantivo']

class ProtoFrasesNewAdmin(admin.ModelAdmin):
  list_display = ['protofrase','extracao','frase']

class ExtracaoNewAdmin(admin.ModelAdmin):
  list_display = ['protofrase', 'frase', 'peso','corte','irse','rep_tema','irgs','rep_geral']

class TestaPalavraAdmin(admin.ModelAdmin):
  list_display = ['palavra','numero','condicao', 'resultado']

class ParametrosDeAjusteAdmin(admin.ModelAdmin):
  list_display = ['radio_r', 'faixa_histo','check_grau','check_betw','check_eigen','permitir_RT','num_tweets', 'acuidade','ident','k_betweenness','dr_delta_min', 'f_corte','f_min_bigramas']

class DadosExtracaoNewAdmin(admin.ModelAdmin):
  list_display = ['tema','protofrase', 'sentenca','irse','irse_p','irgs','irgs_p']



admin.site.register(CorrigePalavra, CorrigePalavraAdmin)
admin.site.register(ListaDeAdjacencias, ListaDeAdjacenciasAdmin)
admin.site.register(ListaDeSubstantivos, ListaDeSubstantivosAdmin)
admin.site.register(TextoPreproc, TextoPreprocAdmin)
admin.site.register(DadosPreproc, DadosPreprocAdmin)
admin.site.register(ListaVertices, ListaVerticesAdmin)
admin.site.register(TabelaRanking, TabelaRankingAdmin)
admin.site.register(DadosSelecaoTemas, DadosSelecaoTemasAdmin)
admin.site.register(PesosEAlpha, PesosEAlphaAdmin)
admin.site.register(TemasNew, TemasNewAdmin)
admin.site.register(ProtoFrasesNew, ProtoFrasesNewAdmin)
admin.site.register(ExtracaoNew, ExtracaoNewAdmin)
admin.site.register(DadosExtracaoNew, DadosExtracaoNewAdmin)
admin.site.register(TestaPalavra, TestaPalavraAdmin)
admin.site.register(ParametrosDeAjuste, ParametrosDeAjusteAdmin)
