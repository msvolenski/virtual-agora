from django.contrib import admin
from .models import SentencasExtraidas, MapasTemasESubtemas, Clusters, CorrigePalavra, TextoPreproc,ParametrosDeAjuste, ListaDeSubstantivos, DadosPreproc,TestaPalavra, ListaVertices, TabelaRanking, ListaDeAdjacencias, TemasNew, SentencasAvaliadas

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
  list_display = ['corretor','id','palavras_por_sentenca_lssw', 'palavras_por_sentenca_org','quantidade_de_sentencas','palavras_texto_original', 'palavras_texto_lematizado','palavras_texto_lematizado_ssw','nome_rel_protofrase']

class TabelaRankingAdmin(admin.ModelAdmin):
  list_display = ['vertice_nome','vertice_numero','grau', 'grau_norm', 'betweenness','betweenness_norm','eigenvector','eigenvector_norm', 'potenciacao']

class ListaDeAdjacenciasAdmin(admin.ModelAdmin):
  list_display = ['vertice_i','vertice_f','peso']

class TemasNewAdmin(admin.ModelAdmin):
  list_display = ['tema','classificacao' ,'irt']

class ListaDeSubstantivosAdmin(admin.ModelAdmin):
  list_display = ['palavra','substantivo']

class SentencasAvaliadasAdmin(admin.ModelAdmin):
  list_display = ['tema', 'subtema', 'proto', 'frase', 'peso', 'corte', 'irse']
  
class SentencasExtraidasAdmin(admin.ModelAdmin):
  list_display = ['tema','subtema', 'frase', 'peso','corte','irse','representatividade']

class TestaPalavraAdmin(admin.ModelAdmin):
  list_display = ['palavra','numero','condicao', 'resultado']

class ParametrosDeAjusteAdmin(admin.ModelAdmin):
  list_display = ['radio_r', 'faixa_histo','permitir_RT','num_tweets', 'ident','k_betweenness', 'f_corte','f_min_bigramas']

class MapasTemasESubtemasAdmin(admin.ModelAdmin):
  list_display = ['ident','tema', 'subtema', 'grau','irt_l','fim_de_arvore']
  
class ClustersAdmin(admin.ModelAdmin):
  list_display = ['etapa', 'ident','caminho','nucleos','subtemas','q_subtemas', 'situacao','fim_de_arvore']


admin.site.register(CorrigePalavra, CorrigePalavraAdmin)
admin.site.register(ListaDeAdjacencias, ListaDeAdjacenciasAdmin)
admin.site.register(ListaDeSubstantivos, ListaDeSubstantivosAdmin)
admin.site.register(TextoPreproc, TextoPreprocAdmin)
admin.site.register(DadosPreproc, DadosPreprocAdmin)
admin.site.register(ListaVertices, ListaVerticesAdmin)
admin.site.register(TabelaRanking, TabelaRankingAdmin)
admin.site.register(TemasNew, TemasNewAdmin)
admin.site.register(SentencasAvaliadas, SentencasAvaliadasAdmin)
admin.site.register(TestaPalavra, TestaPalavraAdmin)
admin.site.register(ParametrosDeAjuste, ParametrosDeAjusteAdmin)
admin.site.register(Clusters, ClustersAdmin)
admin.site.register(MapasTemasESubtemas, MapasTemasESubtemasAdmin)
admin.site.register(SentencasExtraidas, SentencasExtraidasAdmin)

