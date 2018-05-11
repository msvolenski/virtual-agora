from django.conf.urls import url

from . import views

app_name = 'extrator'
urlpatterns = [


    
   
    url(r'^graph$', views.GraphTestView.as_view(), name='graphtest'),
    url(r'^extrator/$', views.ResultadosExtratorHomeView.as_view(), name='resultadosextratorHome'),
    url(r'^extrator/lematizar$', views.lematizar, name='lematizador'),
    url(r'^extrator/dados$', views.inserir_dados_de_entrada, name='dados'),
    url(r'^extrator/dadostwitter$', views.inserir_dados_de_entrada_twitter, name='dados_twitter'),
    url(r'^extrator/stopwords$', views.eliminar_stopwords, name='stopwords'),
    url(r'^extrator/preproc$', views.pre_processamento, name='preproc'),  
    url(r'^extrator/salvar$', views.salvar_dados, name='salvar'),
    url(r'^extrator/salvarDadosIniciais$', views.salvar_dados_iniciais, name='salvar_iniciais'),
    url(r'^extrator/limparIgnoradas$', views.limpar_palavras_ignoradas, name='limpar_ignoradas'),
    url(r'^extrator/carregarls$', views.carregar_ls, name='carrega_ls'),
    url(r'^extrator/relatorio$', views.gerar_relatorio, name='relatorio'),    
    url(r'^extrator/passos2$', views.executa_passo_2, name='executa_passo_2'),
    url(r'^extrator/passos4$', views.executa_passo_4, name='executa_passo_4'),
    url(r'^extrator/passos5$', views.executa_passo_5, name='executa_passo_5'),
    url(r'^extrator/passos6$', views.executa_passo_6, name='executa_passo_6'),
    url(r'^extrator/resultado/(?P<passo>[-\w]+)/$', views.mostra_resutados, name='mostra_resultados'),
    url(r'^extrator/listavertices$', views.lista_de_vertices, name='lista_vertices'),
    url(r'^extrator/mapear$', views.mapear, name='mapear'),
    url(r'^extrator/redecomplexa$', views.rede_complexa, name='rede_complexa'),
    url(r'^extrator/matriz$', views.matriz, name='matriz'),
    url(r'^extrator/corretor$', views.corretor_ortografico, name='corretor'),
    url(r'^extrator/atualizacorretor/(?P<palavra_correta>(.+))/(?P<posicao>(\d+))/(?P<opcao>[\w\-]+)$', views.atualiza_corretor_ortografico, name='atualiza_corretor'),
    url(r'^extrator/passo3$', views.executa_passo_3, name='executa_passo_3'),
    url(r'^extrator/metricasranking$', views.metricas_e_ranking, name='metricas_ranking'),    
    url(r'^extrator/mapeareextrair$',views.mapearEextrair, name='mapear_e_extrair'),
    url(r'^extrator/indicerepresentatividade$', views.calcula_indice_representatividade, name='calculair'),
    url(r'^extrator/processarprotofrases$', views.processarProtofrases, name='processarpfs'),      
    url(r'^extrator/calcularindice/$', views.calcula_indice, name='calularindice'),
    url(r'^extrator/selecionartemas/$', views.selecionar_temas, name='selecionar_temas'),
    url(r'^extrator/extraisglobais/$', views.extraiSentencasGlobais, name='eglobais'),
    url(r'^extrator/agrupartemas/$', views.agrupar_temas, name='agrupar_temas'),
    url(r'^extrator/limpasubstantivo/(?P<opcao>[-\w]+)/$', views.limpar_lista_subtantivos, name='limpar_lista_subtantivos'),
    url(r'^extrator/ajustarparametro/(?P<opcao>[-\w]+)/$', views.ajustar_parametro, name='ajustar_parametro'),
    url(r'^extrator/testeuser/$', views.testa_substantivo_usuario, name='testa_substantivo_usuario'),
    url(r'^extrator/mapaeresultadostemas/$', views.gerarMapaEResultados, name='gerar_mapa_resultados'),
    url(r'^extrator/extrairnucleos/$', views.extrairNucleos, name='extrair_nucleos'),
    #url(r'^extrator/testee/$', views.teste, name='teste'),
]


