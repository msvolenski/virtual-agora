from django.conf.urls import url

from . import views

app_name = 'extrator'
urlpatterns = [
    url(r'^extrator/$', views.ExtratorHomeView.as_view(), name='extratorHome'),

    url(r'^extrator/lematizar$', views.lematizar, name='lematizador'),
    url(r'^extrator/verarquivo/(?P<arquivo>[-\w]+)/$', views.ver_arquivo, name='ver_arquivo'),
    url(r'^extrator/dados$', views.inserir_dados_de_entrada, name='dados'),
    url(r'^extrator/dadostwitter$', views.inserir_dados_de_entrada_twitter, name='dados_twitter'),
    url(r'^extrator/stopwords$', views.eliminar_stopwords, name='stopwords'),
    url(r'^extrator/preproc$', views.pre_processamento, name='preproc'),  
    url(r'^extrator/salvar$', views.salvar_dados, name='salvar'),
    url(r'^extrator/salvarDadosIniciais$', views.salvar_dados_iniciais, name='salvar_iniciais'),
    url(r'^extrator/limparIgnoradas$', views.limpar_palavras_ignoradas, name='limpar_ignoradas'),
    url(r'^extrator/relatorio$', views.gerar_relatorio, name='relatorio'),
    url(r'^extrator/passo2$', views.executar_passo_2, name='executar_passo_2'),
    url(r'^extrator/passo3$', views.executar_passo_3, name='executar_passo_3'),
    url(r'^extrator/passo4$', views.executar_passo_4, name='executar_passo_4'),
    url(r'^extrator/passo5$', views.executar_passo_5, name='executar_passo_5'),
    url(r'^extrator/passos2a5$', views.executar_passos_2_a_5, name='executar_passos_2_a_5'),
    url(r'^extrator/listavertices$', views.lista_de_vertices, name='lista_vertices'),
    url(r'^extrator/mapear$', views.mapear, name='mapear'),
    url(r'^extrator/matriz$', views.matriz, name='matriz'),
    url(r'^extrator/corretor$', views.corretor_ortografico, name='corretor'),
    url(r'^extrator/atualizacorretor/(?P<palavra_correta>(.+))/(?P<posicao>(\d+))/(?P<opcao>[\w\-]+)$', views.atualiza_corretor_ortografico, name='atualiza_corretor'),
    url(r'^extrator/rede$', views.rede_complexa, name='rede_complexa'),
    url(r'^extrator/metricasranking$', views.metricas_e_ranking, name='metricas_ranking'),    
    url(r'^extrator/mapeareextrair$',views.mapearEextrair, name='mapear_e_extrair'),
    url(r'^extrator/indicerepresentatividade$', views.calcula_indice_representatividade, name='calculair'),
    url(r'^extrator/processarprotofrases$', views.processarProtofrases, name='processarpfs'),      
    url(r'^extrator/mostratabela/(?P<tipo>[-\w]+)/$', views.mostra_tabela, name='mostra_tabela'),   
    url(r'^extrator/calcularindice/$', views.calcula_indice, name='calularindice'),
    url(r'^extrator/selecionartemas/$', views.selecionar_temas, name='selecionar_temas'),
]
