# -*- coding: utf-8 -*-
from __future__ import division
from .models import DadosSelecaoTemas, ParametrosDeAjuste, TextoPreproc, ListaDeSubstantivos, TestaPalavra, DadosPreproc, ListaVertices, TabelaRanking, ListaDeAdjacencias, PesosEAlpha, TemasNew, ProtoFrasesNew, ExtracaoNew, DadosExtracaoNew
from collections import OrderedDict, Counter
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from math import log
from nltk.tokenize import TweetTokenizer
from PIL import Image
import aspell
import codecs
import emoji
import networkx as nx
import math
import matplotlib
import matplotlib.pyplot as plt
import nltk
import numpy as np
import operator
import os
import platform
import pylab
import powerlaw
import re
import subprocess
import time
import tweepy




# Create your views here.
class RelatorioPreprocHomeView(generic.ListView):
  template_name = 'extrator/relatoriopreproc.html'
  #model = Topic
  def get_queryset(self):
     #u = User.objects.get(user=self.request.user)
     return #Topic.objects.filter(published='Sim',projeto__sigla=u.user.user.projeto).distinct()


class ExtratorHomeView(generic.ListView):
  template_name = 'extrator/extrator_home.html'
  #model = Topic
  def get_queryset(self):

    return #Topic.objects.filter(published='Sim',projeto__sigla=u.user.user.projeto).distinct()

class ResultadosExtratorHomeView(generic.ListView):
  template_name = 'extrator/extrator_resultados.html'
  
  def get_queryset(self):
    return  
  
 
def inserir_dados_de_entrada(request):
    #CRIA/lÊ O ARQUIVO ONDE SERÁ INSERIDO OS DADOS DE ENTRADA
    
    #inicia cronometro
    inicio = time.time() 
    
    if os.path.exists("extrator/arquivos/p1_texto_inicial_original.txt"):
            programName = "C:/Program Files/Notepad++/notepad++.exe"
            fileName = "extrator/arquivos/p1_texto_inicial_original.txt"
            subprocess.Popen([programName, fileName])
            dados_de_entrada = codecs.open("extrator/arquivos/p1_texto_inicial_original.txt","r","utf-8").read()
            
            #finaliza tempo
            tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
            return render(request, 'extrator/extrator_resultados.html', {'tempo_p1vd':tempo_total, 'goto':'passo1','muda_logo':'logo_vis_dados'})
    else:
        file_doc_original = codesc.open("extrator/arquivos/p1_texto_inicial_original.txt","w","utf-8")
        file_doc_original.close()
        programName = "C:/Program Files/Notepad++/notepad++.exe"
        fileName = "extrator/arquivos/p1_texto_inicial_original.txt"
        subprocess.Popen([programName, fileName])
        dados_de_entrada = codecs.open("extrator/arquivos/p1_texto_inicial_original.txt","r","utf-8").read()
        
        #finaliza tempo
        tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
        return render(request, 'extrator/extrator_resultados.html', {'tempo_p1vd':tempo_total, 'goto':'passo1','muda_logo':'logo_vis_dados'})


def inserir_dados_de_entrada_twitter(request):
    #inicia cronometro
    inicio = time.time() 
    
    #define documento de entrada
    entrada_tweets_copia = codecs.open("extrator/arquivos/p1_texto_inicial_original.txt","w", "utf-8")
    
    #busca palavra digita e testa sua existencia
    hashtag = request.POST['hashtag']
    if not hashtag:
        
        #finaliza tempo
        tempo_total =  ("{0:.4f}".format(time.time() - inicio))          
        return render(request, 'extrator/extrator_home.html', {'dados_de_entrada': None})

    #busca dados no twitter
    consumer_key = 'NfaYz4Enkx2V2tOsjCv2lSiyr'
    consumer_secret = 'jwGB1ppEFsMkYldOSszCAE1j6paib0IolFn02dBQJM5g1u5AvQ'
    access_token = '493595634-6Qv9H8bBkRJ8FHme6yHu3HW4BUmVHLjYXXqWqOic'
    access_token_secret = '7bxNoz9El5H9w2Af0jx3pXiWvQuiBCggkoFwmQHkeuYRt'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)    
    api = tweepy.API(auth)

    #variaveis
    num_tweets = 500
    contador_tweets = 0
    max_id = 0
    tweets_por_busca = 100
    fim = 'nao'

    #primeira Busca - Define o ultimo_id
    public_tweets = api.search(q=hashtag ,lang='pt', count=100, result_type='recent')
    ultimo_id = public_tweets[-1].id
    
    #salva primeiros tweets
    for tweet in public_tweets:          
        try: 
            tweet.retweeted_status
                #print tweet.retweeted_status.text
        except:
            a = 1
        
        if contador_tweets < num_tweets:
            entrada_tweets_copia.write(tweet.text)
            entrada_tweets_copia.write(str(contador_tweets))
            entrada_tweets_copia.write('\n\n')
            contador_tweets += 1
            print tweet.id   
         
    print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    while fim == 'nao':       
            public_tweets = api.search(q=hashtag ,lang='pt', count=100, max_id=(ultimo_id - 1))   
            for tweet in public_tweets:
                #try: 
                 #   tweet.retweeted_status
                    #print tweet.retweeted_status.text
                #except:
                 #   a = 1
                #print tweet.id
                if contador_tweets < num_tweets:
                    entrada_tweets_copia.write(tweet.text)
                    entrada_tweets_copia.write(str(contador_tweets))
                    entrada_tweets_copia.write('\n\n')
                    contador_tweets += 1
                    print tweet.id
                else:
                    fim = 'sim' 
                print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                 
            ultimo_id = public_tweets[-1].id    
       
    
    entrada_tweets_copia.close() 
    
    

    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))   
   
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p1dt':tempo_total,'goto':'passo1','muda_logo':'logo_twitter'})


def salvar_dados_iniciais(request):
    #inicia cronometro
    inicio = time.time()
    
    #inicializa as flags de controle
    r = DadosPreproc.objects.get(id=1)
    r.flag_testapalavra = 'nao'
    r.flag_completo = 'nao'
    r.save()
    
    #Separa tokens para processamento do documento
    entrada_original = codecs.open("extrator/arquivos/p1_texto_inicial_original.txt","r", "utf-8")
    entrada_tokenizada1 = codecs.open("extrator/arquivos/p1_texto_inicial_tokens.txt","w", "utf-8")
    entrada_tokenizada2 = codecs.open("extrator/arquivos/p2_texto_inicial_tokens_corrigido.txt","w", "utf-8")

    #grava tokens nos novos arquivos  
    documento = entrada_original.read()

    #resolve problema dos links do twiiter
    documento = documento.replace(r'https:',r'https')
    
    
    #elimina os mais ainda malditos emoticons
    myre = re.compile('('
            '\ud83c[\udf00-\udfff]|'
            '\ud83d[\udc00-\ude4f\ude80-\udeff]|'
            '[\u2600-\u26FF\u2700-\u27BF])+'.decode('unicode_escape'), 
            re.UNICODE)            
    documento = myre.sub('emoticon',documento)      
    
    #tokenizer para Tweets
    tknzr = TweetTokenizer()
    palavras = tknzr.tokenize(documento)    
      
    for i,token in enumerate(palavras): 
        #elinina os links malditos do twitter
        myre = re.compile("t.co.")
        eh_link = myre.match(token)
        if not eh_link:                    
            entrada_tokenizada1.write(token)
            entrada_tokenizada2.write(token)
            entrada_tokenizada1.write(' ')
            entrada_tokenizada2.write(' ')      
    entrada_original.close()
    entrada_tokenizada1.close()
    entrada_tokenizada2.close()

    #zera o corretor
    try:
        execucao = DadosPreproc.objects.get(id=1)
        execucao.corretor = 'off'
        execucao.save()      
    except:
        DadosPreproc.objects.create(id=1, corretor='off',flag_testapalavra='nao')
   
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p1sd':tempo_total,'goto':'passo1','muda_logo':'logo_salvar_dados'})


def corretor_ortografico(request):
    #inicia cronometro
    inicio = time.time()
    
    # Lê documento a ser corrigido
    arquivo = codecs.open("extrator/arquivos/p2_texto_inicial_tokens_corrigido.txt", "r", "utf-8")
    documento = arquivo.read()
    palavras = documento.split(' ')
    
    #inicializa o corretor
    corretor = aspell.Speller('lang','pt_BR') 

    #Lê arquivo de palavras ignoradas
    if os.path.exists("extrator/arquivos/p2_lista_palavrasIgnoradas.txt"):
        arquivo_np = codecs.open("extrator/arquivos/p2_lista_palavrasIgnoradas.txt", "r", "utf-8")
        doc = arquivo_np.read()
        palavras_ignoradas = nltk.word_tokenize(doc)           
    else:
        arquivo_np = codecs.open("extrator/arquivos/p2_lista_palavrasIgnoradas.txt", "w", "utf-8")
        palavras_ignoradas = []         

    #inicia análise das palavras pelo corretor
    posicao = 0
    for palavra in palavras:
           
        #Testa se o token é uma palavra (formada por letras)
        pattern = re.compile("(?:[.A-Za-z0-9áãõÃÕéóíúàèìòùêâîôûÂÊÎÔÛÁÉÍÓÚÀÈÌÒÙÇç-]+)$")        
        eh_palavra = pattern.match(palavra.encode('utf-8'))                
            
        if eh_palavra:
            #testa se a palavra está no dicionario        
            res = corretor.check(palavra.encode("iso-8859-1"))

            #condição caso a palavra nao estiver no dicionário                
            if res == 0 and palavra not in palavras_ignoradas: 
                sugestoes = []
                sugestoes_codificadas = []  
                sugestoes = corretor.suggest(palavra.encode("iso-8859-1"))
                    
                #e codifica as palavras
                for item in sugestoes:                                            
                    sugestoes_codificadas.append(item.decode('iso-8859-1'))
                arquivo.close()
                arquivo_np.close()               
                return render(request, 'extrator/extrator_resultados.html', {'popup': 'sim','palavra':palavra , 'lista_de_sugestoes':sugestoes_codificadas, 'posicao':posicao})    
            
        posicao = posicao + 1
        
    #finaliza o corretor
    arquivo.close() 
    arquivo_np.close() 

    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))    
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p1co':tempo_total ,'goto':'passo1','muda_logo':'logo_corretor'})


def atualiza_corretor_ortografico(request,palavra_correta,posicao,opcao):
    #abre arquivo a ser corrigido
    arquivo = codecs.open("extrator/arquivos/p2_texto_inicial_tokens_corrigido.txt", "r", "utf-8")
    documento = arquivo.read()
    palavras = documento.split(' ')
    
    #inicializa corretor
    corretor = aspell.Speller('lang','pt_BR')

    #Ignora a palavra
    if opcao == 'opcao0':
        arquivo_pa = codecs.open("extrator/arquivos/p2_lista_palavrasIgnoradas.txt", "a", "utf-8")
        arquivo_pa.write(palavra_correta)
        arquivo_pa.write(' ')
        arquivo_pa.close()
        return corretor_ortografico(request)    
    
    #inclui palavra ao dicionário  
    if opcao == 'opcao1': 
        corretor.addtoPersonal(palavra_correta.encode("iso-8859-1"))
        corretor.saveAllwords()           
        return corretor_ortografico(request)        
           
    #troca palavra do texto inicial por palavra escolhida pelo usuário
    if opcao == 'opcao2':             
        arq_atualiza = codecs.open("extrator/arquivos/p2_texto_inicial_tokens_corrigido.txt", "w", "utf-8")        
        buffer1 = list(palavras)
        buffer1[int(posicao)]=palavra_correta
        palavras=' '.join(buffer1)        
        c = 0
        for ii in palavras.split(' '):            
            arq_atualiza.write(ii)            
            arq_atualiza.write(' ')
            c = c + 1        
        arq_atualiza.close()
        return corretor_ortografico(request) 
    
    #troca palavra do texto por palavra digitada pelo usuário e inclui nova palavra no dicionário
    if opcao == 'opcao3':
        #palavra recebe a palavra digitada para ser incluida no dicionário
        palavra_correta = request.POST['sugestao_usr']
        
        #Determina o tipo de substituição
        try:
            tipo = request.POST["substituir"]
            tipo = "apenas_esta_palavra"
        except:
            tipo = "todas_as_ocorrencias"
        
        if tipo == "apenas_esta_palavra":
            arq_atualiza = codecs.open("extrator/arquivos/p2_texto_inicial_tokens_corrigido.txt", "w", "utf-8")        
            buffer1 = list(palavras)
            buffer1[int(posicao)]=palavra_correta
            palavras=' '.join(buffer1)        
            for ii in palavras.split(' '):
                arq_atualiza.write(ii)            
                arq_atualiza.write(' ')             
            arq_atualiza.close()
            return corretor_ortografico(request)
        
        if tipo == "todas_as_ocorrencias":
            arq_atualiza = codecs.open("extrator/arquivos/p2_texto_inicial_tokens_corrigido.txt", "w", "utf-8")            
            correcao =[]
            for word in palavras:
                if word == palavras[int(posicao)]:
                    arq_atualiza.write(palavra_correta)
                    arq_atualiza.write(' ')
                    correcao.append(palavra_correta)                    
                else:
                    arq_atualiza.write(word)
                    arq_atualiza.write(' ')
                    correcao.append(word)           
            arq_atualiza.close()
            return corretor_ortografico(request)

    #Inclui palavra à lista de stop-words
    if opcao == 'opcao4':
        arquivo_sw = codecs.open("extrator/arquivos/p2_lista_stopwords.txt", "a", "utf-8")
        arquivo_sw.write(palavra_correta)
        arquivo_sw.write('\n')
        arquivo_sw.close()
        return corretor_ortografico(request)       
    
    return render(request, 'extrator/extrator_resultados.html', {'goto':'passo1'})


def limpar_palavras_ignoradas(request):
    lista = codecs.open("extrator/arquivos/p2_lista_palavrasIgnoradas.txt","w","utf-8")
    lista.write('')
    lista.close()  
    return render(request, 'extrator/extrator_home.html', {'dados_de_entrada': None})


def pre_processamento(request):
    #inicia cronometro
    inicio = time.time()

    #Tokeniza o texto e escreve em documento único.
    arq_texto_preproc = codecs.open('extrator/arquivos/p2_texto_preprocessado.txt','w','utf-8')
    arq_texto_preproc_vet = file_org = codecs.open("extrator/arquivos/p2_texto_preprocessado_vetorizado.txt","w",'utf-8')
    arq_texto_inicial = codecs.open("extrator/arquivos/p2_texto_inicial_tokens_corrigido.txt", "r", "utf-8")
    texto_inicial = arq_texto_inicial.read()    

    #elimina pontuação repetida
    texto_inicial = re.sub(r'[\?\.\!\;]+(?=[\?\.\!\;])', '', texto_inicial)
   
    #Separa os tokens
    #tokenizer para Tweets
    tknzr = TweetTokenizer()
    tokens = tknzr.tokenize(texto_inicial)      
    
    #conta número de palavras
    contador = 0
    for token in tokens:
        pattern = re.compile("(?:[A-Za-z0-9áãõÃÕéóíúàèìòùêâîôûÂÊÎÔÛÁÉÍÓÚÀÈÌÒÙÇç-]+)$") #considera palavra os tokens que contém uma combinação destes caracteres       
        eh_palavra = pattern.match(token.encode('utf-8'))
        if eh_palavra:
            contador = contador + 1 

    #Conta o número de sentenças e escreve tokens nos arquivos
    pontuacao = [".","!","(",")",":",";","<","=",">","?","[","]","{","|","}"]    
    sentencas = 0
    for item in tokens:        
        if item in pontuacao:
            item = "."
            sentencas = sentencas + 1
        item_l = item.lower()
        
        #elimina todo item que tem o ... do twitter substituindo por um ponto final
        pattern = re.compile(ur'.*…')
        eh_palavra = pattern.match(item_l)
        if eh_palavra:
            item_l = '.' 
        
        #elimina tudo que possui http substituindo por um ponto final
        pattern = re.compile(ur'^http')
        eh_palavra = pattern.match(item_l)
        if eh_palavra:
            item_l = '.'
               
       
        arq_texto_preproc.write(item_l + " ")
        arq_texto_preproc_vet.write(item_l + '\n')
    arq_texto_preproc.close()
    arq_texto_preproc_vet.close()
    arq_texto_inicial.close()

    #Salva dados no Banco de dados
   
    dados_preprocessamento = DadosPreproc.objects.get(id=1)
    dados_preprocessamento.quantidade_de_sentencas = sentencas
    dados_preprocessamento.palavras_texto_original = str(contador)
    dados_preprocessamento.save()
    
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
   
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p2pd':tempo_total,'muda_logo':'logo_preparar_dados','goto':'passo2'})


def lematizar(request):
    #inicia cronometro
    inicio = time.time()

    #Abre o Bash e executa o lematizador no texto inicial
    is32bit = (platform.architecture()[0] == '32bit')
    system32 = os.path.join(os.environ['SystemRoot'],
                        'SysNative' if is32bit else 'System32')
    bash = os.path.join(system32, 'bash.exe')
    start_time = time.time()
    p = subprocess.check_call('"%s" -c "cd Linguakit-master ; ./linguakit pt lem ../extrator/arquivos/p2_texto_preprocessado.txt > ../extrator/arquivos/p2_saida_lematizador.txt ; unix2dos ../extrator/arquivos/p2_saida_lematizador.txt"' % bash, shell=True)
    temp =  time.time() - start_time
    
    #abre o texto já lematizado e cria dois novos arquivos: um com o texto original e outro com o texto lematizado
    saida_lematizador = codecs.open("extrator/arquivos/p2_saida_lematizador.txt","r","utf-8")
    texto_lematizado = codecs.open("extrator/arquivos/p2_texto_lematizado.txt","w",'utf-8')
    texto_lematizado_vetor = codecs.open("extrator/arquivos/p2_texto_lematizado_vetor.txt","w",'utf-8')
    file_tags = open("extrator/arquivos/arquivo_tags.txt","w")

    #Pega a palavra lematizada no documento de saída do lematizador
    contador = 0
    for linha in saida_lematizador:        
        try:
            linha.split(' ')[2]
            word_lem = linha.split(' ')[1]
            texto_lematizado.write(word_lem + ' '),
            texto_lematizado_vetor.write(word_lem + '\n'),
            
            #contador de palavras
            pattern = re.compile("(?:[A-Za-z0-9áãõÃÕéóíúàèìòùêâîôûÂÊÎÔÛÁÉÍÓÚÀÈÌÒÙÇç-]+)$") #considera palavra os tokens que contém uma combinação destes caracteres       
            eh_palavra = pattern.match(word_lem.encode('utf-8'))
            if eh_palavra:
                contador = contador + 1 
     
        except:
            word_lem = linha.split(' ')[0]           
            texto_lematizado.write(word_lem + ' '),
            texto_lematizado_vetor.write(word_lem + '\n'),
           
            #contador de palavras
            pattern = re.compile("(?:[A-Za-z0-9áãõÃÕéóíúàèìòùêâîôûÂÊÎÔÛÁÉÍÓÚÀÈÌÒÙÇç-]+)$") #considera palavra os tokens que contém uma combinação destes caracteres       
            eh_palavra = pattern.match(word_lem.encode('utf-8'))
            if eh_palavra:
                contador = contador + 1
    texto_lematizado_vetor.close()
    texto_lematizado.close()
    
    #Salva quantidade de palavras no banco de dados
    
    dados_preprocessamento = DadosPreproc.objects.get(id=1)
    dados_preprocessamento.palavras_texto_lematizado = str(contador)
    dados_preprocessamento.save()  
    
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p2le':tempo_total,'goto': 'passo2', 'muda_logo':'logo_lematizar'})    


def eliminar_stopwords(request):
    #inicia cronometro
    inicio = time.time()

    #Lê arquivo de stop-words e cria uma lista
    if os.path.exists("extrator/arquivos/p2_lista_stopwords.txt"):
        arq_stopwords = codecs.open("extrator/arquivos/p2_lista_stopwords.txt", "r", "utf-8")
        lista_de_stopwords = arq_stopwords.read()
        stopwords = tokens = nltk.word_tokenize(lista_de_stopwords)
    else:
        
        return render(request, 'extrator/extrator_home_2.html', {'dados_de_entrada': None})
    
    #lê texto lematizado
    arq_texto = codecs.open("extrator/arquivos/p2_texto_lematizado.txt", "r", "utf-8")
    texto = arq_texto.read()
    palavras = texto.split(' ')

    #gera arquivos de saída
    arq_saida = codecs.open("extrator/arquivos/p2_texto_lematizado_ssw.txt","w", "utf-8")
    arq_saida_vetor = codecs.open("extrator/arquivos/p2_texto_lematizado_ssw_vetor.txt","w", "utf-8")
    
    #verifica se a palavra é uma stop-word, grava palavras no arquvivo e conta número de palavras
    contador = 0
    for palavra in palavras:        
        if palavra not in stopwords:
            arq_saida.write(palavra)
            arq_saida.write(' ')
            arq_saida_vetor.write(palavra)
            arq_saida_vetor.write('\n')
            
            #contador de palavras
            pattern = re.compile("(?:[A-Za-z0-9áãõÃÕéóíúàèìòùêâîôûÂÊÎÔÛÁÉÍÓÚÀÈÌÒÙÇç-]+)$") #considera palavra os tokens que contém uma combinação destes caracteres       
            eh_palavra = pattern.match(palavra.encode('utf-8'))
            if eh_palavra:
                contador = contador + 1 
    arq_saida.close()
    arq_saida_vetor.close() 

    #Salva quantidade de palavras do texto SSW no BD
    
    dados_preprocessamento = DadosPreproc.objects.get(id=1)
    dados_preprocessamento.palavras_texto_lematizado_ssw = str(contador)
    dados_preprocessamento.save()        
    
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p2es':tempo_total,'goto':'passo2','muda_logo':'logo_eliminar_sw'  })    


def salvar_dados(request):
    #inicia cronometro
    inicio = time.time()
    
    #Pega objetos-texto e reinicializa o BD para receber novo texto
    texto_passo1 = TextoPreproc.objects.all()
    texto_passo1.delete()
    
    #salvando via bulk
    tokens = codecs.open("extrator/arquivos/p2_texto_lematizado_ssw_vetor.txt", "r", "utf-8").readlines()
    for t in tokens:
        
        t.encode('utf-8')
        
    aList = [TextoPreproc(vertice=token.rstrip('\n'), vertice_num=-1) for token in tokens]    
    TextoPreproc.objects.bulk_create(aList)
    
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p2sb':tempo_total,'goto': 'passo2','muda_logo':'logo_salvar_bd' })


def gerar_relatorio(request):
    #inicia cronometro
    inicio = time.time()
    
    #inicializações: cria arquivo do relatório e pega dados no BD
    dadosPreprocessamento = DadosPreproc.objects.get(id=1)
    arq_relatorio = codecs.open("extrator/arquivos/p2_relatorio.txt","w")

    arq_relatorio.write("RELATÓRIO DA ETAPA DE PRÉ-PROCESSAMENTO \n\n")
    arq_relatorio.write("Os dados de entrada contém " + str(dadosPreprocessamento.quantidade_de_sentencas) + " parágrafos.\n")
    arq_relatorio.write("Os dados de entrada possuem " + dadosPreprocessamento.palavras_texto_original + " palavras.\n")
    arq_relatorio.write("Os dados lematizados possuem " + dadosPreprocessamento.palavras_texto_lematizado + " palavras.\n")
    
    #Apresenta no relatório as palavras não lematizadas
    new_list = []
    file = codecs.open("extrator/arquivos/p2_saida_lematizador.txt","r",'utf-8')
    for line in file:
        try:
            line.split(' ')[2]
        except:
            word_lem = line.split(' ')[0]
            new_list.append(word_lem)
    if not new_list:
        arq_relatorio.write("Não houveram erros durante a lematização.\n")
    else:
        arq_relatorio.write("Palavras não lematizadas: ")
        for i in new_list:
            arq_relatorio.write(i.encode('utf-8') + " " )
        arq_relatorio.write("\n")    
    
    arq_relatorio.write("O documento lematizado e sem stopwords possui " + dadosPreprocessamento.palavras_texto_lematizado_ssw + " palavras.\n\n")
    arq_relatorio.write("CONCLUSãO:\n")
    comp = 100 - (float(dadosPreprocessamento.palavras_texto_lematizado_ssw)/float(dadosPreprocessamento.palavras_texto_original))*100
    arq_relatorio.write("Compressão do texto após pré-processamento: " + str(comp) + " %.\n")
    pal_sen_org = round(float(int(dadosPreprocessamento.palavras_texto_original))/float(dadosPreprocessamento.quantidade_de_sentencas))
    dadosPreprocessamento.palavras_por_sentenca_org = int(pal_sen_org)    
    arq_relatorio.write("Em média, cada sentença do texto original possui " + str(int(pal_sen_org)) + " palavras.\n")
    pal_sen_lemssw = round(float(int(dadosPreprocessamento.palavras_texto_lematizado_ssw))/float(dadosPreprocessamento.quantidade_de_sentencas))
    dadosPreprocessamento.palavras_por_sentenca_lssw = int(pal_sen_lemssw)    
    arq_relatorio.write("Em média, cada sentença do texto lematizado sem stop-words possui " + str(int(pal_sen_lemssw)) + " palavras.\n")
    arq_relatorio.close()
    
    #salva calculos no BD
    dadosPreprocessamento.save()
   
    #LÊ relatório    
    p2_relatorio = codecs.open("extrator/arquivos/p2_relatorio.txt","r","utf-8").read()

    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p2gr':tempo_total,'goto': 'passo2','muda_logo':'logo_gerar_rp2'})


## PASSO 3. REDE COMPLEXA -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def lista_de_vertices(request):
    #inicia cronometro
    inicio = time.time()
            
    #Objtivo: Criar uma lista com todos os vertices distintos e associa-los a um número (indice)
    
    #Exclui todos os objetos da ListaVertices para receber novos objetos
    ListaVertices.objects.all().delete()

    #Cria dicionário com todos os vertices distintos e seu indice   
    pontos_finais = [".\n","!\n","?\n",":\n",";\n",".","!","?",":",";"]
    vertices = {}    
    objs = TextoPreproc.objects.exclude(vertice__in=pontos_finais).values_list('vertice', flat=True).distinct()
    index = 0
   
    for item in objs:
        if item != '\n':
            vertices[index] = item
            index = index + 1
    
    #Salva no BD via bulk    
    aList = [ListaVertices(index = key, node = element.strip()) for key,element in vertices.iteritems()]    
    ListaVertices.objects.bulk_create(aList) 
    
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio)) 
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p3dv':tempo_total,'goto': 'passo3', 'muda_logo':'logo_def_vertices' })

def mapear(request):
    #inicia cronometro
    inicio = time.time()
            
    #Objetivo: Associar cada palavra do texto lematizado ao seu respectivo indice

    #carrega objetos
    palavras = TextoPreproc.objects.all().values_list('vertice','vertice_num')
    #print palavras
    vertices_nome = ListaVertices.objects.all().values_list('node', flat=True)
    vertices_nome = list(vertices_nome)
    vertices_numero = ListaVertices.objects.all().values_list('index',flat=True)
    vertices_numero = list(vertices_numero)    
    
    #cria listas para mapear
    lista_texto = []
    for palavra in palavras:
        try:
            indice = vertices_nome.index(palavra[0].strip())
            numero = vertices_numero[indice]
            lista_texto.append((palavra[0].strip(),numero))
        except:           
            numero = -1
            lista_texto.append((palavra[0].strip(),numero))    
   
    #Testa se a lista de palavras mapeadas tem o mesmo tamanho da lista de objetos de texto pre processado  
    if len(lista_texto) != len(palavras):  
         
        #finaliza tempo
        tempo_total =  ("{0:.4f}".format(time.time() - inicio))    
        return render(request, 'extrator/extrator_resultados.html', {'tempo_p1vd':tempo_total,'goto':'passo3','muda_logo_error':'logo_indexar'})       
    
    #armazena no BD
    TextoPreproc.objects.all().delete()
    aList = [TextoPreproc(vertice=linha[0].strip(), vertice_num=linha[1]) for linha in lista_texto]    
    TextoPreproc.objects.bulk_create(aList)    
    
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p3ip':tempo_total,'goto': 'passo3' , 'muda_logo':'logo_indexar'})


def matriz(request):
    #inicia cronometro
    inicio = time.time()
    
    #Objetivo: gera a lista de adjacencias a partir de uma matriz de adjacências

    #Inicializa arquivos
    arq_listaAdjacencias = codecs.open("extrator/arquivos/p3_lista_adjacencias.txt","w",'utf-8')
    arq_subdocumento = codecs.open("extrator/arquivos/p3_texto_sentencas.txt",'w','utf-8')
    
    #inicializa e carrega dados do BD
    ListaDeAdjacencias.objects.all().delete()  
    tokens = TextoPreproc.objects.all()
    
    #Gera documento de sentencas    
    for token in tokens:       
        if token.vertice == '.':
            arq_subdocumento.write('\n')
        else:
            arq_subdocumento.write(token.vertice)
            arq_subdocumento.write(' ')
    arq_subdocumento.close()   
    
    #lÊ documento de sentenças
    sentencas = codecs.open('extrator/arquivos/p3_texto_sentencas.txt','r','utf-8').read().splitlines()

    #cria lista de adjancecias
    lista_adjacencias = OrderedDict()
    for sentenca in sentencas:
        palavras_sentenca = sentenca.split(' ')
        for i, palavra in enumerate(palavras_sentenca):
            try:
                palavras_sentenca[i+2]                            
                bigrama = palavras_sentenca[i] + ' ' + palavras_sentenca[i+1]
            except:
                bigrama = 'fim' 
            if bigrama != 'fim':
                try:   
                    lista_adjacencias[bigrama] = lista_adjacencias[bigrama] + 1
                except:
                    lista_adjacencias[bigrama] = 1 

    #salva lista de adjacencias em arquivo
    for k,v  in lista_adjacencias.items():
        vertices = k.split(' ')        
        arq_listaAdjacencias.write(k + ' ' + str(float(v)) + '\n')
    arq_listaAdjacencias.close()

    #salva lista de adjacencias no BD
    aList = [ListaDeAdjacencias(vertice_i=k.split(' ')[0], vertice_f=k.split(' ')[1],peso=v) for k,v in lista_adjacencias.items()]    
    ListaDeAdjacencias.objects.bulk_create(aList)       
    
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p3gr':tempo_total,'goto':'passo3','muda_logo':'logo_rede'})


def rede_complexa(request):
    
    #Lê arquivo que contém a lista de adjacenicas
    arq_listaAdjacencias = codecs.open("C:/virtual-agora/extrator/arquivos/p3_lista_adjacencias.txt","r","utf-8")
    listaAdjacencias = arq_listaAdjacencias.readlines()
    
    #carrega lista de vertices
    lista_de_vertices = ListaVertices.objects.all()

    #gera rede
    rede = nx.DiGraph()
    for vertice in lista_de_vertices:
        rede.add_node(vertice.node)
    for bigrama in listaAdjacencias:                
        vertice_inicial = bigrama.split(' ')[0]
        vertice_final =  bigrama.split(' ')[1]
        peso =  float(bigrama.split(' ')[2])
        rede.add_edge(vertice_inicial , vertice_final , weight = peso)
    
    #Visualização da rede
    pos = nx.spring_layout(rede)
    labels = nx.get_edge_attributes(rede,'weight')
    nx.draw_networkx_edge_labels(rede,pos,edge_labels=labels)
    nx.draw(rede, pos,edge_labels=labels, with_labels = True)    
    plt.show()
    plt.close()
    
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    
    return render(request, 'extrator/extrator_home_3.html', {'tempo_p1vd':tempo_total,'dados_de_entrada': None, 'relatorio_preproc':None })    


## PASSO 4. MÉTRICAS E RANKING  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def metricas_e_ranking(request): 
    #inicia cronometro
    inicio = time.time()

    #Objetivo: calcular as métricas de centralidade da rede e gerar tabelas    
    
     #carrega parametros de ajuste
    try:
        parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
        
    except ObjectDoesNotExist:
        parametros = ParametrosDeAjuste(ident=1,k_betweenness=100,dr_delta_min=5,f_corte=10,f_min_bigramas=50)
        parametros.save()

    #Lê arquivo que contém a lista de adjacenicas
    arq_listaAdjacencias = codecs.open("C:/virtual-agora/extrator/arquivos/p3_lista_adjacencias.txt","r","utf-8")
    listaAdjacencias = arq_listaAdjacencias.readlines()

    #Cria arquivos para receber as tabelas
    arq_tabela_graus = codecs.open("extrator/arquivos/p4_tabela_graus.txt", 'w', 'utf-8')
    arq_tabela_betweenness = codecs.open("extrator/arquivos/p4_tabela_betweenness.txt", 'w','utf-8')
    arq_tabela_closeness = codecs.open("extrator/arquivos/p4_tabela_closeness.txt", 'w','utf-8')
    arq_texto_vertices = codecs.open("extrator/arquivos/p4_texto_vertices.txt", 'w','utf-8')

    #Prepara banco de dados para receber as tabelas
    tabelas = TabelaRanking.objects.all()
    tabelas.delete()

    #carrega lista de vertices
    lista_de_vertices = ListaVertices.objects.all()

    #gera rede
    rede = nx.DiGraph()
    for vertice in lista_de_vertices:
        rede.add_node(vertice.node)
    for bigrama in listaAdjacencias:                
        vertice_inicial = bigrama.split(' ')[0]
        vertice_final =  bigrama.split(' ')[1]
        peso =  float(bigrama.split(' ')[2])
        rede.add_edge(vertice_inicial , vertice_final , weight = peso)
    
    
    #gera tabelas
    print "calculando métrica graus..."
    tabela_graus = nx.degree(rede, weight='weight')    
    print "calculando métrica betweenness..."
    tabela_betweenness = nx.betweenness_centrality(rede, weight='weight', normalized=False, k=int(float(parametros.k_betweenness/100)*len(rede.nodes())))    
    #tabela_closeness = nx.closeness_vitality(rede,weight='weight' )
    print "calculando métrica closeness..."
    tabela_closeness = nx.closeness_centrality(rede) 
    print 'fim'
    #encontra maiores valores de grau, betweenness e cloasennes
    maior_grau = max(tabela_graus.iteritems(), key=operator.itemgetter(1))[1]
    maior_betweenness = max(tabela_betweenness.iteritems(), key=operator.itemgetter(1))[1]
    maior_closeness = max(tabela_closeness.iteritems(), key=operator.itemgetter(1))[1]
    
    #cria lista de vertices
    vertices = nx.nodes(rede)

    #gera dicionarios de valores normalizados e cria um texto de vertices (para o próximo passo)
    tabela_grau_normalizado = {}
    tabela_betweenness_normalizado = {}
    tabela_closeness_normalizado = {}    
    for vertice in vertices:        
        arq_texto_vertices.write(vertice + ' ')
        tabela_grau_normalizado[vertice] = tabela_graus.get(vertice)/maior_grau
        tabela_betweenness_normalizado[vertice] = tabela_betweenness.get(vertice)/maior_betweenness
        tabela_closeness_normalizado[vertice] = tabela_closeness.get(vertice)/maior_closeness

    #Armazenando Tabelas no BD via Bulking 
    aList = [TabelaRanking(vertice_nome = vertice.rstrip('\n'), vertice_numero=ListaVertices.objects.get(node__exact=vertice).index, grau=tabela_graus[vertice], grau_norm=tabela_grau_normalizado[vertice], 
        betweenness=tabela_betweenness[vertice], betweenness_norm=tabela_betweenness_normalizado[vertice], 
        closeness=tabela_closeness[vertice], closeness_norm=tabela_closeness_normalizado[vertice], potenciacao=1.0) for vertice in vertices]
    TabelaRanking.objects.bulk_create(aList)

    #gera Tabelas Ranking
    tabela_graus_ordenada = TabelaRanking.objects.all().order_by('-grau')    
    tabela_betweenness_ordenada = TabelaRanking.objects.all().order_by('-betweenness')    
    tabela_closeness_ordenada = TabelaRanking.objects.all().order_by('-closeness')
    
    #Salva ranking graus em arquivo
    for linha in tabela_graus_ordenada:
        arq_tabela_graus.write(linha.vertice_nome + ' ' + str(linha.grau) + ' ' + str(linha.grau_norm) + '\n')
    
    #Salva ranking betweenness em arquivo
    for linha in tabela_betweenness_ordenada:
        arq_tabela_betweenness.write(linha.vertice_nome + ' ' + str(linha.betweenness) + ' ' + str(linha.betweenness_norm) + '\n')
    
    #Salva ranking closeness em arquivo
    for linha in tabela_closeness_ordenada:
        arq_tabela_closeness.write(linha.vertice_nome + ' ' + str(linha.closeness) + ' ' + str(linha.closeness_norm) + '\n') 

    #fecha arquivos
    arq_tabela_graus.close()
    arq_tabela_betweenness.close()
    arq_tabela_closeness.close()
    arq_texto_vertices.close()   
    
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p4cm':tempo_total,'goto': 'passo4', 'muda_logo':'logo_calc_metricas' }) 


def calcula_indice(request):
    #inicia cronometro
    inicio = time.time()
    
    #OBJETIVO: definir a forma de calcular a potenciacao (seus pesos) e gerar a tabela potenciacao
    matplotlib.use('agg')
    #Abre arquivo de dados a serem lidos
    tabela_grau = codecs.open("extrator/arquivos/p4_tabela_graus.txt").readlines()
    tabela_betweenness = codecs.open("extrator/arquivos/p4_tabela_betweenness.txt").readlines()
    tabela_closeness = codecs.open("extrator/arquivos/p4_tabela_closeness.txt").readlines()
    
    #Carrega dados do BD
    vertices_objs = ListaVertices.objects.all()
    tabela_ranking_completa = TabelaRanking.objects.all()
    try:
        td =  DadosSelecaoTemas.objects.get(id=1)                      
    except:
        DadosSelecaoTemas.objects.create(id=1,delta=0,f=0,fb=0,p_grau=0,p_bet=0,p_clos=0)
        td =  DadosSelecaoTemas.objects.get(id=1)
           
    #Inicializa arquivos a serem escritos
    arq_tabela_potenciacao = codecs.open("extrator/arquivos/p4_tabela_potenciacao.txt", 'w', 'utf-8')    
    arq_matriz_pesos = codecs.open("extrator/arquivos/p4_matriz_pesos.txt", 'w', 'utf-8')
    arq_relatorio = codecs.open("extrator/arquivos/p4_relatorio_potenciacao.txt", 'w')   
   
    #Prepara o BD para receber os novos pesos
    pesos = PesosEAlpha.objects.all()
    pesos.delete()
    
    #gera matriz de pesos
    var = 0.1
    for a1 in range(0,12):
        for a2 in range(0,12):
            a3 = 10 - a1 - a2
            if a3 >= 0 and a1 != 0 and a2 != 0 and a3 != 0:
                arq_matriz_pesos.write(str(a1*var) + ' ')
                arq_matriz_pesos.write(str(a2*var) + ' ')
                arq_matriz_pesos.write(str(a3*var) + ' ')
                arq_matriz_pesos.write('\n')
    arq_matriz_pesos.close()

    ## FIM ETAPA 2 ####################################################
    ## ETAPA 3: SELEÇÃO DOS PESOS DAS MÉTRICAS ########################

    # abre matriz de pesos
    pesos = codecs.open("extrator/arquivos/p4_matriz_pesos.txt").readlines()

    #inicializa matlibplot para duas figuras e cores
    rgb_a=5
    rgb_b=94
    rgb_c=200

    #calculo de alpha para cada conjunto de peso
    for peso in pesos:
        pgra = float(peso.split(' ')[0])
        pbet =  float(peso.split(' ')[1])
        pclo = float(peso.split(' ')[2])

        # CALCULA POTENCIAÇÃO
        tabela_potenciacao_temp = {}
        for vertice in vertices_objs:
            grau_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).grau_norm
            bet_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).betweenness_norm
            clo_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).closeness_norm
            potenciacao = float(pgra)*float(grau_n) + float(pbet)*float(bet_n) + float(pclo)*float(clo_n)
            tabela_potenciacao_temp[vertice.node] = potenciacao
        
        # Cria uma tabela vertice(nome)-indice
        tabela_potenciacao_temp_ordenada = {}
        tabela_potenciacao_temp_ordenada = sorted(tabela_potenciacao_temp.items(),key=lambda x: x[1], reverse=True)

        # exclui os 5% ultimos temas quando pertinente (n>0)
        corte = 0.00
        numero_vertices_excluidos = int(corte*len(tabela_potenciacao_temp_ordenada))
        if numero_vertices_excluidos > 0:            
            del tabela_potenciacao_temp_ordenada[-numero_vertices_excluidos:]
        
        #exclui vertice de indice zero       
        flag = 'on'
        while flag == 'on':        
            for i,v in enumerate(tabela_potenciacao_temp_ordenada):
                flag = 'off'
                if v[1] == 0.0:
                    flag = 'on'
            if flag == 'on':
                del tabela_potenciacao_temp_ordenada[-1:]

        #Faz a regressão linear e calcula alpha da tabela
        valores_potenciacao = [valor[1] for valor in tabela_potenciacao_temp_ordenada]        
        fit = powerlaw.Fit(valores_potenciacao)
       
        #calcula o MLF dos dados (o quão ajustados estão)
        # maximum likelihood fitting (MLF)
        soma = 0
        for p in valores_potenciacao:
            soma = soma + log(float(p)/float(fit.xmin))
        alpha_esperado = -1*(1 + len(tabela_potenciacao_temp_ordenada)*(1.0/soma))
        
        # Caclula o erro entre alpha e MLF
        erro = (abs(fit.alpha - alpha_esperado)/fit.alpha)*100
    
        #plota gráfico
        eixo_y = list(range(len(tabela_potenciacao_temp_ordenada)))
        
        #CHAMA FUNÇÃO QUE PLOTA FIGURAS
        plota_figura(eixo_y,valores_potenciacao,rgb_a,rgb_b,rgb_c,fit.alpha,'plota_figura_1','endereco')        
        
        #_test_chart(eixo_y,valores_potenciacao,rgb_a,rgb_b,rgb_c,fit.alpha,'plota_figura_1','endereco')       
        rgb_a = (rgb_a + 50)%255
        rgb_b = (rgb_b + 10)%255
        rgb_c = (rgb_c+ 80)%255
    
        #armazena os pesos, alpha, MLF e erro no BD
        resultado = PesosEAlpha(p_grau = pgra , p_betw = pbet, p_close = pclo , alpha = fit.alpha, alphaesp = alpha_esperado, erro = erro)
        resultado.save()        

    #CHAMA FUNÇÃO QUE SALVA FIGURAS   
    plota_figura('x','x','x','x','x','x','salva_figura_1','extrator/arquivos/p4_grafico_alphas.png')    
  
    #Busca pesos de menor erro e maior valor alpha ( para erro < 1%)
    corte_erro = 0
    pesos_selecionados = []
    while not pesos_selecionados:
        lista_de_erros = []
        lista_de_erros = PesosEAlpha.objects.all().filter(erro__lt=corte_erro).order_by('alpha')
        pesos_selecionados = lista_de_erros.last()
        corte_erro = corte_erro + 1
        if pesos_selecionados:
            corte_erro = corte_erro - 1

    #salvar dados com parÂmetros escolhidos
    td.p_grau= pesos_selecionados.p_grau 
    td.p_clos= pesos_selecionados.p_close
    td.p_bet = pesos_selecionados.p_betw
    td.save()

    #Monta a Tabela de Indices com o Peso encontrado e salva no BD
    pgra =  pesos_selecionados.p_grau
    pbet =   pesos_selecionados.p_betw
    pclo =  pesos_selecionados.p_close

    #CALCULA POTENCIAÇÃO
    tabela_potenciacao_temp = {}
    for vertice in vertices_objs:
        grau_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).grau_norm
        bet_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).betweenness_norm
        clo_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).closeness_norm
        potenciacao = float(pgra)*float(grau_n) + float(pbet)*float(bet_n) + float(pclo)*float(clo_n)
        #Salva na Tabela Ranking
        tabela = TabelaRanking.objects.get(vertice_nome__iexact = vertice.node)
        tabela.potenciacao = potenciacao
        tabela.save()    

    #salva a tabela de indice em um arquivo em ordem alfabética e cria figura
    tabela_potenciacao_ordenada = TabelaRanking.objects.all().order_by('-potenciacao')
    tabela_potenciacao_ordenada_valores = []
    eixo_y = list(range(len(tabela_potenciacao_ordenada)))   
    
    for linha in tabela_potenciacao_ordenada:        
        index = ListaVertices.objects.get(node__exact=linha.vertice_nome).index
        arq_tabela_potenciacao.write(str(index) + ' ' + linha.vertice_nome + ' ' + str(linha.potenciacao) + ' ' + '\n')        
        tabela_potenciacao_ordenada_valores.append(linha.potenciacao)
 
    #Chama função que plota o grafico  
    plota_figura(eixo_y,tabela_potenciacao_ordenada_valores,'black','x','x','x','plota_e_salva_figura_2','extrator/arquivos/p4_grafico_alpha_selecionado.png')   

    ## FIM ETAPA 3 #######################################################
    ## GERA RELATÒRIO ####################################################
   
    arq_relatorio.write('RELATÓRIO FINAL - TABELA ÍNDICE\n\n\n')   
    arq_relatorio.write('ETAPA 1 - DETERMINANDO OS PESOS DAS MÉTRICAS\n')
    arq_relatorio.write('   - Método: Melhor ajuste à Lei da Potência\n')
    arq_relatorio.write('   - Entrada: Matriz de pesos-candidato\n')
    arq_relatorio.write('              Variação: 0.1 à 0.9 em ' + str(var) + '\n')
    arq_relatorio.write('              Restrição: soma dos pesos = 1\n\n')
    arq_relatorio.write('   - Ajuste à lei de potência\n')
    arq_relatorio.write('              Dados: Exclui os ' + str(corte*100) + '% últimos vértices - ' +  str(numero_vertices_excluidos) + ' vértices.\n')
    arq_relatorio.write('              Cálculo de Alpha: Métodos dos mínimos quadrados\n')
    arq_relatorio.write('              Alpha de ajuste:: Maximun Likelihood fitting\n')
    arq_relatorio.write('              Erro = |alpha de ajuste - alpha| \n\n')
    arq_relatorio.write('   - Resultado\n')
    arq_relatorio.write('              Alpha / Alpha de ajuste / erro (%) / Pesos \n')
    lista_de_alphas = PesosEAlpha.objects.all().order_by('alpha')
    for la in lista_de_alphas:
        arq_relatorio.write('              ' + str(la.alpha) + ' / ' + str(la.alphaesp) + ' / ' + str(la.erro) + ' / ' + str(la.p_grau) + ' ' + str(la.p_betw) + ' ' + str(la.p_close) + ' \n')
    arq_relatorio.write('\n              Corte: erro > ' + str(corte_erro) + ' % \n\n')
    arq_relatorio.write('              Alpha / Alpha de ajuste / erro (%) / Pesos \n')
    for li in lista_de_erros:
        arq_relatorio.write('              ' + str(li.alpha) + ' / ' + str(li.alphaesp) + ' / ' + str(li.erro) + ' / ' + str(li.p_grau) + ' ' + str(li.p_betw) + ' ' + str(li.p_close) + ' \n')
    arq_relatorio.write('\n              Maior alpha: ' + str(pesos_selecionados.alpha) + ' \n')
    arq_relatorio.write('              Pesos selecionados: Graus: ' + str(pesos_selecionados.p_grau) + ' ; Betweeness: ' + str(pesos_selecionados.p_betw) + ' ; Closeness: ' + str(pesos_selecionados.p_close) + ' \n\n')
    arq_relatorio.write('ETAPA 2 - TABELA RANKING\n')
    arq_relatorio.write('   palavra - índice\n\n')
    for linha in tabela_potenciacao_ordenada:
        arq_relatorio.write(linha.vertice_nome.encode('utf-8') + ' - ' + str(linha.potenciacao) + '\n')

    #fecha arquivos
    arq_relatorio.close()
    arq_tabela_potenciacao.close()
    
    rel_ind = codecs.open("extrator/arquivos/p4_relatorio_potenciacao.txt","r",'utf-8').read()
    
     #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p4ci':tempo_total,'goto': 'passo4', 'muda_logo':'logo_calc_indice'})


def plota_figura(eixoY,eixoX,cor1,cor2,cor3,alpha,tipo,endereco):

    #Lógica maluca
    if tipo == 'salva_figura_1':        
        pylab.savefig(endereco)       
        plt.clf()
        return
    if tipo == 'plota_figura_1':       
        pylab.plot(eixoY, eixoX, 'ro',  markersize = 1, color=(cor1/255.0,cor2/255.0,cor3/255.0), label=alpha)
        return 
    if tipo == 'plota_e_salva_figura_2':
        pylab.plot(eixoY, eixoX, 'ro', markersize = 1, color=cor1)
        pylab.savefig(endereco)       
        return


def selecionar_temas(request):
    #inicia cronometro
    inicio = time.time()
                    
    #carrega parametros de ajuste
    try:
        parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
        
    except ObjectDoesNotExist:
        parametros = ParametrosDeAjuste(ident=1,k_betweenness=100,dr_delta_min=5,f_corte=10,f_min_bigramas=50)
        parametros.save()
    
    #carrega dados
    dados = DadosSelecaoTemas.objects.get(id=1)
    r =  DadosPreproc.objects.get(id=1)

    #inicializa arquivos a serem escritos e lidos
    arq_relatorio = codecs.open("extrator/arquivos/p4_relatorio_temas.txt", 'w')    
    arq_lematizador = codecs.open('extrator/arquivos/p2_saida_lematizador.txt','r','utf-8')
    arq_distancias = codecs.open("extrator/arquivos/p4_relatorio_distancias_relativas.txt", 'w')
    tabela_potenciacao = codecs.open("extrator/arquivos/p4_tabela_potenciacao.txt").readlines()

    #inicializa dados do BD
    TemasNew.objects.all().delete()
    
    #calculo da frequencia absoluta de corte  
    f = int(float(parametros.f_corte/100)*len(tabela_potenciacao))    
    
    tabela_bigramas = ListaDeAdjacencias.objects.all()
    tabela_potenciacao_objs = TabelaRanking.objects.all().order_by('-potenciacao')    
    
    #cria listas e dicionários
    tabela_potenciacao_numeros = OrderedDict()
    distancias_relativas_novo = OrderedDict()
    vertices_selecionados = OrderedDict()
    temas_preselecionados = OrderedDict()
    tabela_graus_entrada = OrderedDict()
    temas_excluidos = []    
    
    #inicializa relatório
    arq_relatorio.write('RELATÓRIO FINAL - TEMAS')
    arq_relatorio.write('\n\n\n')
    arq_relatorio.write('ETAPA 1: PRÉ-SELEÇÃO DOS TEMAS')
    arq_relatorio.write('\n\n')
    arq_relatorio.write('- Métrica: ' + str(dados.p_grau) + '%' + ' graus; '+ str(dados.p_bet) + '%' + ' betwenness; '+ str(dados.p_clos) + '%' + ' closeness;' + '\n' )    
    
    #cria tabela com indice potenciação
    for linha in tabela_potenciacao:
        tabela_potenciacao_numeros[linha.split(' ')[0]] = float(linha.split(' ')[2].rstrip('\n'))     
    
    #Calcula as distÂncias relativas entre os vértices da tabela potenciacao
    for index, numero in enumerate(tabela_potenciacao_numeros):        
        potenciacao_inicial = tabela_potenciacao_numeros.values()[index]
        try:
            potenciacao_final = tabela_potenciacao_numeros.values()[index+1]
        except:
            break        
        try:
            distancias_relativas_novo[tabela_potenciacao_numeros.keys()[index] + '->' + tabela_potenciacao_numeros.keys()[index+1]] = 100*((potenciacao_inicial - potenciacao_final)/potenciacao_inicial) 
        except:
            distancias_relativas_novo[tabela_potenciacao_numeros.keys()[index] + '->' + tabela_potenciacao_numeros.keys()[index+1]] = 0 
        try:
            arq_distancias.write(tabela_potenciacao_numeros.keys()[index] + '->' + tabela_potenciacao_numeros.keys()[index+1] + ' = ' + str(100*((potenciacao_inicial - potenciacao_final)/potenciacao_inicial)) + '\n' )        
        except:
            arq_distancias.write(tabela_potenciacao_numeros.keys()[index] + '->' + tabela_potenciacao_numeros.keys()[index+1] + ' = 0 \n')

    
    #gera o grafico das distancias relativas
    matplotlib.rc('font', family='Arial')    
    objects = distancias_relativas_novo.keys()    
    y_pos = np.arange(len(objects))    
    performance = distancias_relativas_novo.values()
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Distancia relativa') 
    plt.title('Distancias Relativas dos nos da rede')
    pylab.savefig('extrator/arquivos/p4_grafico_distancias_relativas_potenciacao.png')     
   
    #Passo 1: selecionando os vertices mais significaivos (fora da cauda longa)    

    #procura início da cauda    
    contador = 0
    cauda_encontrada = 'nao'
    #inicio_cauda = distancias_relativas_novo.keys()[-1].split('->')[1]
    inicio_cauda = distancias_relativas_novo.keys()[-1]    
    
    for index, vertices in enumerate(distancias_relativas_novo):      
        if contador == f:
            cauda_encontrada = 'sim'
            break
        if distancias_relativas_novo.values()[index] <= parametros.dr_delta_min and contador < f:
            contador = contador + 1
        if distancias_relativas_novo.values()[index] > parametros.dr_delta_min:
            contador = 0        
            inicio_cauda = vertices 
     
    
    #Seleciona região fora da cauda e armazena vertices (nomes e numeros)    
    vertice_inicio_cauda = inicio_cauda.split('->')[1]
        
    for linha in tabela_potenciacao_objs:
        vertices_selecionados[linha.vertice_numero] = linha.vertice_nome
        if str(linha.vertice_numero) == str(vertice_inicio_cauda):
            break
   
    #Pré-seleciona os temas excluindo os não-substantivos #########################################################    
    
    #armazena palavras para iniciar o teste  
    if r.flag_testapalavra.strip() == 'nao': 
        TestaPalavra.objects.all().delete()
        aList = [TestaPalavra(palavra = nome, numero=int(numero), condicao='aguardando', resultado='null') for numero,nome in vertices_selecionados.items()]    
        TestaPalavra.objects.bulk_create(aList)
        r.flag_testapalavra = 'sim'
        r.save()                
      
    #inicializa flag de execucao
    flag_fim = 'nao'  
    
    #Verifica se há palavras a serem testadas
    palavras = TestaPalavra.objects.filter(condicao__exact='aguardando').values_list('palavra',flat=True)   
    
    if not palavras:    
        flag_fim = 'sim'             
        
    while flag_fim == 'nao':        
        lista_substantivos = ListaDeSubstantivos.objects.all().values_list('palavra','substantivo')
        lista_palavras = ListaDeSubstantivos.objects.all().values_list('palavra', flat=True)
        arq_lematizador = codecs.open('extrator/arquivos/p2_saida_lematizador.txt','r','utf-8')
        palavras_lematizadas = arq_lematizador.readlines()  
        
        for palavra in palavras:
            tags = [] 
            pal = TestaPalavra.objects.get(palavra__exact=palavra)    
            
            #Busca todas as tags possíveis para a palavra
            for linha in palavras_lematizadas:            
                tokens = linha.strip().split(' ')            
                if palavra in tokens:                           
                    for token in tokens:            
                        pattern = re.compile("^[A-Z].")
                        eh_tag = pattern.match(token)
                        if eh_tag:
                            tags.append(token)
                    
            #verifica se todas as referências são à substantivo
            repeticoes = 0
            for tag in tags:
                pattern = re.compile("^N|U")
                eh_substantivo = pattern.match(tag)
                if eh_substantivo:
                    repeticoes += 1        
            
            #caso a palavra seja substantivo, atualiza BD 
            if palavra in lista_palavras:
                #analise se a palavra esta na lista de substantivos
                for key, value in lista_substantivos:
                    if palavra == key:
                        cond = value
                        pal.condicao = 'finalizado'
                        pal.resultado = cond
                        pal.save()                     
            
            elif len(tags) == repeticoes:            
                pal.condicao = 'finalizado'
                pal.resultado ='sim'
                pal.save()

            #caso nao haja classificação como sunstantivo, atualiza BD 
            elif repeticoes == 0:
                pal.condicao = 'finalizado'
                pal.resultado ='nao'
                pal.save()
            
            #Na impossibilidade de vertificar, pergunta ao usuário            
            else:                
                if r.flag_completo == 'sim':
                    return palavra    
                else:                           
                    return render(request, 'extrator/extrator_resultados.html', {'testa_sub':'sim' , 'palavra_candidata':palavra})
        flag_fim = 'sim'
                

    #ao termino, atualiza execuçao para off    
    r.flag_testapalavra = 'nao'
    r.save()
 

    #cria vetor de vertices selecionados
    temas_preselecionados = TestaPalavra.objects.filter(resultado='sim').values_list('numero','palavra')
    temas_preselecionados = OrderedDict(temas_preselecionados)
            
    #escreve relatório
    arq_relatorio.write('- Parâmetros: ' + 'delta: ' + str(parametros.dr_delta_min) + '%; ' + 'f: ' + str(parametros.f_corte) + '% dos nós totais (' + str(f) + ' nós)' + '\n' )
    arq_relatorio.write('- Temas pré-selecionados' + '(' + str(len(temas_preselecionados)) +'):' + '\n\n')
    for tema in temas_preselecionados.values():
        arq_relatorio.write(tema.encode('utf-8') + '\n')

    #passo 2: definindo os nós-temas baseado na vizinhança e frequencia
    arq_relatorio.write('\n\nETAPA 2: SELEÇÃO FINAL DOS TEMAS\n\n')
    arq_relatorio.write('- Metodologia: Vizinho grau-1 \ frequência relativa dos bi-gramas\n')
    arq_relatorio.write('- Parâmetro: fb(frequência mínima de bigramas): ' + str(parametros.f_min_bigramas) + "% do total de bigramas\n")
    arq_relatorio.write('- Resultados: \n\n')
    arq_relatorio.write('Tema  ->  Vizinho  / Peso bigrama em relação ao vizinho / Frequência relativa \n\n')

    # calcula grau de entrada dos temas pre-selecionados      
    for tema in temas_preselecionados.values():
        tema_entradas = tabela_bigramas.filter(vertice_f=tema)
        peso = 0
        for bigrama in tema_entradas:            
            peso = peso + bigrama.peso            
        tabela_graus_entrada[tema] = peso
    
    # verifica se o grau de entrada do vertice-destino é maior que 50% do peso do bigrama e cria lista de vertices a serem excluidos    
    for tema_i in temas_preselecionados.values():
        for tema_f in temas_preselecionados.values():
            bigramas = tabela_bigramas.filter(vertice_i=tema_i,vertice_f=tema_f)            
            for bigrama in bigramas:  
                arq_relatorio.write(bigrama.vertice_i.encode('utf-8') + ' -> ' + bigrama.vertice_f.encode('utf-8') + ' - ' + str(bigrama.peso) + '/' + str(tabela_graus_entrada[tema_f]) + ' - ' +  str((bigrama.peso/tabela_graus_entrada[tema_f])*100) + '%\n')            
                if bigrama.peso >= (parametros.f_min_bigramas*tabela_graus_entrada[tema_f])/100:
                    temas_excluidos.append(tema_f)
    
    temas_selecionados = temas_preselecionados.values()    
    for tema in temas_excluidos:
       temas_selecionados.remove(tema)
       
    #escreve relatório e armazena temas no BD
    arq_relatorio.write('\n- Temas selecionados' + '(' + str(len(temas_selecionados)) + '):' '\n\n')
    for tema in temas_selecionados:
        arq_relatorio.write(tema.encode('utf-8') + '\n')

    #Salva temas no BD via bulk e inicializa protofrases    
    aList = [TemasNew(tema = tema, irt=0.0, irt_p=0.0) for tema in temas_selecionados]    
    TemasNew.objects.bulk_create(aList)
    #aList2 = [ProtoFrasesNew(protofrase = tema) for tema in temas_selecionados]    
    #ProtoFrasesNew.objects.bulk_create(aList2)

    arq_relatorio.write('\n\n- Temas excluídos' + '(' + str(len(temas_excluidos)) + '):' + '\n\n')
    for tema in temas_excluidos:
        arq_relatorio.write(tema.encode('utf-8') + '\n' )

    #fecha arquvos
    arq_relatorio.close()
    arq_lematizador.close()
    arq_distancias.close()
    
    #lê relatório
    rel_temas = codecs.open("extrator/arquivos/p4_relatorio_temas.txt", 'r', 'utf-8').read()
    
    if r.flag_completo == 'sim':
        return 'none'    
    else: 
        r.flag_testapalavra = 'nao'
        r.save() 
        #finaliza tempo
        tempo_total =  ("{0:.4f}".format(time.time() - inicio))                           
        return render(request, 'extrator/extrator_resultados.html', {'tempo_p4st':tempo_total,'goto':'passo4', 'muda_logo':'logo_sel_temas' })
   
##### PASSO 5 ###################################################################################################################################

def processarProtofrases(request):
    #inicia cronometro
    inicio = time.time()

    #carrega parâmetros
    parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)        

    #inicializa arquivo do relatório
    arq_procedimento = codecs.open("extrator/arquivos/p5_relatorio_procedimento.txt","w",'utf-8')
    arq_extracao = codecs.open("extrator/arquivos/p5_relatorio_extracao.txt","w",'utf-8')

    #Inicializa BD de frases
    ExtracaoNew.objects.all().delete()
    
    #carrega protofrases
    temas = TemasNew.objects.all()
    buffer_temas = []

    #Carrega texto lematizado
    tokens = TextoPreproc.objects.all()

    #gera arquivo do sub-docimento
    arq_subdocumento = codecs.open("extrator/arquivos/p5_texto_sub_preprocessado_sentencas.txt",'w','utf-8')
    
    for token in tokens:       
        if token.vertice == '.':
            arq_subdocumento.write('\n')
        else:
            arq_subdocumento.write(token.vertice)
            arq_subdocumento.write(' ')
    arq_subdocumento.close()

    #inicia analise de cada tema
    for tema in temas:        
        #print ('processando o tema ' + tema.tema + '...')
        
        #inicia relatórios
        arq_procedimento.write('TEMA: ' + tema.tema + '\n\n')
        arq_extracao.write('TEMA: ' + tema.tema + '\n\n')

        #armazena tema no BD de protofrases
        ProtoFrasesNew.objects.all().delete()
        pf = ProtoFrasesNew(protofrase = tema.tema, extracao='nao',frase='null')
        pf.save()
                
        #flag de termino do procedomemto (off)
        flag = 'on'
        iteracao = 0
        convergiu_tema = 'nao'
        extracao = []      
        
        while flag == 'on': 
            
            #testa se todas as PFs já extrairam frases
            protofrases = ProtoFrasesNew.objects.filter(extracao = 'nao')
            if not protofrases:
                flag = 'off'                 
                break
            flag = 'on'   
            
            #relatório           
            arq_procedimento.write(' - ITERACAO ' + str(iteracao) + ':\n' + '          proto-frase / tamanho da rede (sentencas) / extraiu?\n ')    
                
            #avalia as protofrases que ainda nao obtiveram extracao
            buffer_pfs = []
            pfn = 0
            memoria_pf = []
            memoria_st = []
            indx = 0
            
            for protofrase in protofrases:
                
                #print ('protofrase ' + str(pfn))                
                
                #separa palavras da protofrase e armazena em uma lista e atualiza subtenas
                palavras = protofrase.protofrase.split(' ')
                subtemas_pre_selecionados = []
                
                #gera sub-documento e recebe o numero de sentencas
                numero_de_sentencas, seten, sentencas = GeraSubDocumento(palavras)                
                
                #relatorio
                arq_procedimento.write('       '  + protofrase.protofrase + '     /     ' + str(numero_de_sentencas) + '    /    ')                  
                
                #print 'armazena protofrases e extração...'
                if numero_de_sentencas == 1:
                    convergiu_tema = 'sim'
                    frase = codecs.open('extrator/arquivos/p5_texto_tema.txt','r','utf-8').readlines()                  
                    extracao.append((tema.tema, protofrase.protofrase,frase[0].strip()))
                    arq_extracao.write(protofrase.protofrase + '      ' + frase[0] + '\n')
                    arq_procedimento.write('sim' + '\n')
                    pfn += 1
                else:                  
                    #Se o conjunto de palavras da pf já foi executado, pega o resultado
                    if set(palavras) in memoria_pf:
                        ind = memoria_pf.index(set(palavras))                                    
                        subtemas_pre_selecionados = memoria_pf[ind] 
                    #senão, chama algoritmo de seleção de temas  
                    else:                                
                        #gera nova rede
                        tgo = GeraRede(request)
                    
                        #seleciona os subtemas
                        subtemas_pre_selecionados = SelecionaSubTemas(tgo)

                        #atualiza memória de execuções   
                        memoria_pf.append(set(palavras))
                        memoria_st.append(set(subtemas_pre_selecionados))
                    
                    #adiciona novas protofrases no buffer 
                    convergiu = 'nao'                   
                    for subtema in subtemas_pre_selecionados:
                        if subtema not in palavras:
                            ultimo_tema = palavras[-1]
                            bigramas = ListaDeAdjacencias.objects.filter(vertice_i__exact=ultimo_tema)
                            possiveis_subtemas = bigramas.values_list('vertice_f', flat=True)                         
                            #só acrescenta subtema se ele for vertice de entrada da ultima palavra da protofrase
                            if subtema in list(possiveis_subtemas):
                                convergiu = 'sim'
                                pf_i = ' '.join(palavras)
                                pf = pf_i + ' ' + subtema
                                buffer_pfs.append(pf)                               
                    if convergiu == 'nao':                       
                        set_count = Counter(elem for elem in sentencas)
                        
                        soma = sum(set_count.values())
                        for k,v in set_count.items():
                            per = int((float(v)/soma)*100)
                            if per >= parametros.acuidade:
                                convergiu_tema = 'sim'
                                arq_procedimento.write('sim - com repeticao' + '\n')
                                frase = codecs.open('extrator/arquivos/p5_texto_tema.txt','r','utf-8').readlines()                  
                                extracao.append((tema.tema, protofrase.protofrase,frase[0].strip()))
                                arq_extracao.write(protofrase.protofrase + '      ' + frase[0] + '\n')  
                            else: 
                                arq_procedimento.write('nullll' + '\n')                       
                    else:
                        arq_procedimento.write(protofrase.extracao + '\n')                
                    pfn += 1     

            print 'atualizando banco de dados...'

            #atualiza protofrases no BD
            arq_procedimento.write('\n\n\n')
            iteracao +=1
            print ('Iteração ' + str(iteracao) )
            if buffer_pfs:
                ProtoFrasesNew.objects.all().delete()
                aList = [ProtoFrasesNew(protofrase=pf, extracao='nao',frase='null') for pf in buffer_pfs]    
                ProtoFrasesNew.objects.bulk_create(aList)
            else:
                ProtoFrasesNew.objects.all().delete()
                            
        
        if convergiu_tema == 'nao':
            f = ExtracaoNew(tema = tema.tema, protofrase = 'tema nao convergiu', frase = 'tema nao convergiu')
            f.save()

        else:           
            aList = [ExtracaoNew(tema = linha[0], protofrase = linha[1] , frase = linha[2] ) for linha in extracao]    
            ExtracaoNew.objects.bulk_create(aList)
        
        arq_procedimento.write('\n\n\n')
        arq_extracao.write('\n\n\n')      
    
    #fecha arquivos
    arq_procedimento.close()
    arq_extracao.close()

    rel_proc = codecs.open("extrator/arquivos/p5_relatorio_procedimento.txt", 'r','utf-8').read()
     
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p5pr':tempo_total,'goto': 'passo5', 'muda_logo':'logo_protofrases' })


def mapearEextrair(request):
    #inicia cronometro
    inicio = time.time()

    #relatorio
    arq_relatorio =codecs.open("extrator/arquivos/p5_relatorio_extracao.txt","w")

    #carrega arquivos
    arq_texto_lematizado = codecs.open("extrator/arquivos/p2_texto_lematizado_ssw.txt","r",'utf-8')
    arq_texto_preprocessado = codecs.open("extrator/arquivos/p2_texto_preprocessado.txt","r",'utf-8')
    
    #carrega os temas
    temas = TemasNew.objects.all()

    #inicializa dados da extrcao
    DadosExtracaoNew.objects.all().delete()
    
    #Verifica as repetições de cada protofrase
    for tema in temas:
        frases = Counter(ExtracaoNew.objects.filter(tema = tema.tema).values_list('frase', flat=True))        
        aList = [DadosExtracaoNew(irgs=0,irgs_p=0,irse=0,irse_p=0,tema=tema.tema, protofrase = key, quantidade = value) for key,value in frases.items()]    
        DadosExtracaoNew.objects.bulk_create(aList)   
            
    #Prepara textos do mapeamento separando as sentencas e tirando os espacoes em branco do começo e do fim (strip)
    sentencas_lem_strip = []
    texto_lematizado = arq_texto_lematizado.read()
    sentencas_lem = texto_lematizado.split('.')
    for sentenca in sentencas_lem:
        sentencas_lem_strip.append(sentenca.strip())
          
    sentencas_pp_strip = [] 
    texto_preprocessado = arq_texto_preprocessado.read()
    sentencas_pp = texto_preprocessado.split('.') 
    for sentenca in sentencas_pp:
        sentencas_pp_strip.append(sentenca.strip())
   
    #teste de mapeamento
    if len(sentencas_lem) != len(sentencas_pp):       
        return render(request, 'extrator/extrator_resultados.html', {'goto':'passo5', 'muda_logo_error':'logo_map_extracao' })

    #inicializa relatorio
    arq_relatorio.write('   RELATÓRIO DE EXTRAÇÃO\n\n\n  tema   /   frase   /   repetições   /   sentença (texto original)\n\n')

    dados = DadosExtracaoNew.objects.all()

    for dado in dados:
      
        try:        
            indice =  sentencas_lem_strip.index(dado.protofrase.strip())
            dado.sentenca = sentencas_pp_strip[indice].strip()
            dado.save()
            arq_relatorio.write('  ' + dado.tema.encode('utf-8') + '  /  ' + dado.protofrase.encode('utf-8') + '  /  ' + str(dado.quantidade) + '  /  ' + dado.sentenca.encode('utf-8') + '\n')
        except:
            dado.sentenca = 'null - nao convergiu'
            dado.save()
            arq_relatorio.write('  ' + dado.tema.encode('utf-8') + '  /  ' + dado.protofrase.encode('utf-8') + '  /  ' + str(dado.quantidade) + '  /  ' + dado.sentenca.encode('utf-8') + '\n')

    arq_relatorio.close()

    rel_ext = codecs.open("extrator/arquivos/p5_relatorio_extracao.txt", 'r','utf-8').read()
         
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p5ex':tempo_total,'goto':'passo5', 'muda_logo':'logo_map_extracao'})


def GeraSubDocumento(palavras):
    
    #print 'gerando subdocumento...'
    #inicializa arquivo do subdocumento
    arq_subtema = codecs.open('extrator/arquivos/p5_texto_tema.txt','w','utf-8')

    #abre sub-documento e separa senteças que contém todos os temas
    sentencas_novas = []
    seten = 'null'
    sentencas = codecs.open("extrator/arquivos/p5_texto_sub_preprocessado_sentencas.txt",'r','utf-8').readlines()
    numero_de_sentencas = 0
    for sentenca in sentencas:        
        palavras_sentenca = sentenca.split(' ')         
        if set(palavras).issubset(palavras_sentenca):
            arq_subtema.write(sentenca)
            seten = sentenca
            numero_de_sentencas += 1 
            sentencas_novas.append(sentenca.strip())       
    arq_subtema.close()

    return numero_de_sentencas, seten, sentencas_novas

def GeraRede(request):
   #print 'gerando rede e calculando métrica...'
    
    sentencas = codecs.open('extrator/arquivos/p5_texto_tema.txt','r','utf-8').read().splitlines()

    #cria lista de adjancecias
    lista_adjacencias = {}
    for sentenca in sentencas:
        palavras_sentenca = sentenca.split(' ')
        for i, palavra in enumerate(palavras_sentenca):
            try:
                palavras_sentenca[i+2]                            
                bigrama = palavras_sentenca[i] + ' ' + palavras_sentenca[i+1]
            except:
                bigrama = 'fim' 
            if bigrama != 'fim':
                try:   
                    lista_adjacencias[bigrama] = lista_adjacencias[bigrama] + 1
                except:
                    lista_adjacencias[bigrama] = 1       
    
   
    #cria rede
    rede = nx.DiGraph()
    for keys,values in lista_adjacencias.items():
        vertice_inicial = keys.split(' ')[0]
        vertice_final =  keys.split(' ')[1]
        peso =  float(values)
        rede.add_edge(vertice_inicial , vertice_final , weight = peso)

    #calcula métrica graus    
    tabela_graus = nx.degree(rede, weight='peso')   
    tabela_buffer = sorted(tabela_graus.items(), key=operator.itemgetter(1), reverse=True)
    tabela_graus_ordenada = OrderedDict(tabela_buffer)

    return tabela_graus_ordenada

def SelecionaSubTemas(tabela_graus_ordenada):
    #carrega parametros de ajuste
    try:
        parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
        
    except ObjectDoesNotExist:
        parametros = ParametrosDeAjuste(ident=1,k_betweenness=100,dr_delta_min=5,f_corte=10,f_min_bigramas=50)
        parametros.save()
        
    #calculo das distancias relativas 
    distancias_relativas_novo = OrderedDict()
    for index, numero in enumerate(tabela_graus_ordenada):        
        grau_inicial = tabela_graus_ordenada.values()[index]
        try:
            grau_final = tabela_graus_ordenada.values()[index+1]
        except:
            break        
        try:
            distancias_relativas_novo[tabela_graus_ordenada.keys()[index] + '->' + tabela_graus_ordenada.keys()[index+1]] = 100*((grau_inicial - grau_final)/grau_inicial) 
        except:
            distancias_relativas_novo[tabela_graus_ordenada.keys()[index] + '->' + tabela_graus_ordenada.keys()[index+1]] = 0 
    
    
    #procura início da cauda
    contador = 0
    cauda_encontrada = 'nao'
    
    #inicializa o inicio da cauda com o último vertice
    els = list(distancias_relativas_novo.items())
    inicio_cauda = els[-1][0]

    #calcula frequencia absoluta de corte    
    f = int(float(parametros.f_corte/100)*len(tabela_graus_ordenada))
    #Parâmetro da definição da cauda
    
    delta = parametros.dr_delta_min #distancia relativa
    f_repeticao = f #quantas vezes a distancia minima deve se repetir para definir comeco da cauda
    for index, vertices in enumerate(distancias_relativas_novo):      
        if contador == f_repeticao:
            cauda_encontrada = 'sim'
            break
        if distancias_relativas_novo.values()[index] <= delta and contador < f_repeticao:
            contador = contador + 1
        if distancias_relativas_novo.values()[index] > delta:
            contador = 0        
            inicio_cauda = vertices 
    
    #Seleciona região fora da cauda e armazena vertices (nomes e numeros)    
    vertices_selecionados = []
    vertice_inicio_cauda = inicio_cauda.split('->')[1]    
    for key, value in tabela_graus_ordenada.items():
        vertices_selecionados.append(key)
        if key == vertice_inicio_cauda:
            break
    
    #Pré-seleciona os temas excluindo os não-substantivos
    temas_selecionados = []
    arq_lematizador = codecs.open('extrator/arquivos/p2_saida_lematizador.txt','r','utf-8')
    palavras_lematizadas = arq_lematizador.readlines()    
    for vertice in vertices_selecionados:
        for linha in palavras_lematizadas:            
            if vertice == linha.split(' ')[1]:                                
                if linha.split(' ')[2][0] == 'N' or linha.split(' ')[2][0] == 'U': 
                    temas_selecionados.append(vertice)       
                    break
    
    return temas_selecionados


def calcula_indice_representatividade(request):
    #inicia cronometro
    inicio = time.time()
    
    #Abre arquivos
    arq_texto_lematizado = codecs.open("extrator/arquivos/p2_texto_lematizado_ssw.txt","r",'utf-8')
    arq_relatorio = codecs.open("extrator/arquivos/p5_relatorio_indices_representatividade.txt","w")
    
    #Carrega Temas
    temas = TemasNew.objects.all()

    #Carrega sentencas
    sentencas_distintas = DadosExtracaoNew.objects.all()

    #Carregas sentencas extraídas
    sentencas_extracao = ExtracaoNew.objects.all()

    #carrega sentenças
    sentencas_lem_strip = []
    texto_lematizado = arq_texto_lematizado.read()
    sentencas_lem = texto_lematizado.split('.')
    for sentenca in sentencas_lem:
        sentencas_lem_strip.append(sentenca.strip())

    #inicializa relatorio
    arq_relatorio.write('RELATÓRIO - ÍNDICES DE REPRESENTATIVIDADE\n\n\n - Índice de Representatividade do Tema (IRT)\n\n      Tema   \   IRT   \   IRT(%)\n')
    
    #CÁLCULO DO IRT E IRT%
    numero_total_sentecas = 0
    numero_sentencas_tema = 0
    for tema in temas:
        for sentenca in sentencas_lem_strip:
            lista_tokens = sentenca.split(' ')
            if len(lista_tokens) == 1 and lista_tokens[0] == u'':             
                'ignore'
            else:
                numero_total_sentecas += 1
                if tema.tema in lista_tokens:
                    numero_sentencas_tema += 1                    
        grau_tema = TabelaRanking.objects.get(vertice_nome__exact=tema.tema).grau_norm      
        irt = (float(grau_tema) + float(numero_sentencas_tema/numero_total_sentecas))/2
        irt_p = irt*100
        numero_sentencas_tema = 0
        numero_total_sentecas = 0
        tema.irt = irt        
        tema.irt_p = irt_p
        tema.save()

    #imprime irt no relatorio em ordem
    irts = TemasNew.objects.order_by('-irt')
    for linha in irts:
        arq_relatorio.write('    ' + linha.tema.encode('utf-8') + '  /  ' + str(linha.irt) + '  /  ' + str(linha.irt_p) + '\n')
    
    #CALCULO IRSE E IRGS
    arq_relatorio.write('\n\n - Índice de Representatividade da Sentença em relação ao tema (IRSE) \n\n')
    for tema in temas:
        arq_relatorio.write(' Tema: ' + tema.tema.encode('utf-8') + '\n\n     Sentença    /    IRSE    /    IRSE(%)\n')

        #separa as sentencas extraidas do tema
        sentencas_tema = DadosExtracaoNew.objects.filter(tema=tema.tema)
        
        #carrega o IRT do tema
        irt = TemasNew.objects.get(tema__exact = tema.tema).irt
        
        #calcula a quantidade de frases extraidas do Tema
        numero_total_s_tema = 0
        for sentenca in sentencas_tema:
            numero_total_s_tema = numero_total_s_tema + sentenca.quantidade  
        
        #calcula o indice
        for sentenca in sentencas_tema:
            if sentenca.protofrase == 'tema nao convergiu':
                sentenca.irse = 0
                sentenca.irse_p = 0
                sentenca.save()
                arq_relatorio.write(sentenca.sentenca.encode('utf-8') + '   /   ' + str(sentenca.irse) + '    /    ' + str(sentenca.irse_p) + '\n\n')
            else:
                irse = float(sentenca.quantidade)/float(numero_total_s_tema)
                irse_p = float(irse*100)            
                sentenca.irse = irse
                sentenca.irse_p = irse_p            
                sentenca.save()
                arq_relatorio.write(sentenca.sentenca.encode('utf-8') + '   /   ' + str(sentenca.irse) + '    /    ' + str(sentenca.irse_p) + '\n\n')

        arq_relatorio.write('\n\n\n')
    arq_relatorio.write('\n\n\n')

    #CALCULO DO IRGS 
    arq_relatorio.write('\n\n - Índice de Representatividade Global da (IRGS) \n\n')
    arq_relatorio.write('     Sentença    /    IRGS    /    IRGS(%)\n')   
    #calcula extracoes ocorreram    
    numero_global_sentencas = 0
    for sentenca in sentencas_distintas:        
        if sentenca.protofrase != 'tema nao convergiu':
            numero_global_sentencas = sentenca.quantidade + numero_global_sentencas
                
    #cria lista lista de sentencas distintas
    sentencas_distintas_quantidade = DadosExtracaoNew.objects.all().values_list('protofrase', flat=True) 
    for k in sentencas_distintas_quantidade:
        sent_objs = DadosExtracaoNew.objects.filter(protofrase__exact= k)
        numero_extracoes = 0
        for sent in sent_objs:
            numero_extracoes = sent.quantidade + numero_extracoes
        for sent in sent_objs:
            if sent.protofrase == 'tema nao convergiu':
                sent.irgs = 0
                sent.irgs_p = 0
                sent.save()
            else:    
                sent.irgs = float(numero_extracoes)/float(numero_global_sentencas)
                sent.irgs_p = 100*sent.irgs
                sent.save()
    
    #RELATORIO
    irgss = DadosExtracaoNew.objects.all().values_list('sentenca','irgs','irgs_p').order_by('-irgs')
    irgss_u = list(set(irgss))  
    irgss_u = sorted(irgss_u, key=lambda x: x[1], reverse=True)  
    for linha in irgss_u:
        arq_relatorio.write(linha[0].encode('utf-8') + '   /   ' + str(linha[1]) + '    /    ' + str(linha[2]) + '\n\n')
    arq_relatorio.close()
      
    rel_repr = codecs.open("extrator/arquivos/p5_relatorio_indices_representatividade.txt", 'r','utf-8').read() 
     
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p5re':tempo_total,'goto':'logo_repres', 'muda_logo':'logo_repres','fim':'fim'})


def testa_substantivo_usuario(request , palavra_candidata):
    resposta = request.POST['opcao_usr']
    r = DadosPreproc.objects.get(id=1)
    

    #carrega palavra do BD 
    pal = TestaPalavra.objects.get(palavra__exact=palavra_candidata)  
    
    if resposta == 'sim':        
        pal.condicao = 'finalizado'
        pal.resultado ='sim'
        pal.save()
        try:
            sub = ListaDeSubstantivos.objects.get(palavra__exact=pal)            
        except:
            sub = ListaDeSubstantivos(palavra=pal.palavra, substantivo='sim')
            sub.save()

    if resposta == 'nao':
        pal.condicao = 'finalizado'
        pal.resultado ='nao'
        pal.save() 
        try:
            sub = ListaDeSubstantivos.objects.get(palavra__exact=pal)
        except:
            sub = ListaDeSubstantivos(palavra=pal.palavra, substantivo='nao')
            sub.save()   
    
    if r.flag_completo == 'nao':
        return selecionar_temas(request)
    else:
        return executar_passos_2_a_5(request)
                
def limpar_lista_subtantivos(request,opcao):
    
    if opcao == 'opdois':    
        ListaDeSubstantivos.objects.all().delete()
    
    if opcao == 'opum':
        arquivo_np = codecs.open("extrator/arquivos/p2_lista_palavrasIgnoradas.txt", "w", "utf-8")
        arquivo_np.write('')
        arquivo_np.close()
        
    return render(request, 'extrator/extrator_resultados.html', {'goto':'ajuste'})
    

def ajustar_parametro(request,opcao):
    
    #carrega parametros de ajuste
    try:
        parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
        
    except ObjectDoesNotExist:
        parametros = ParametrosDeAjuste(ident=1,k_betweenness=100,dr_delta_min=5,f_corte=10,f_min_bigramas=50)
        parametros.save()


    if opcao == 'opcao0':    
        novo_parametro = request.POST['valor_k']
        parametros.k_betweenness = int(novo_parametro)
        parametros.save()
        
    
    if opcao == 'opcao1':            
        novo_parametro = request.POST['valor_delta']
        parametros.dr_delta_min = int(novo_parametro)
        parametros.save()
      
    
    if opcao == 'opcao2':            
        novo_parametro = request.POST['valor_fc']
        parametros.f_corte = int(novo_parametro)
        parametros.save()
       
    
    if opcao == 'opcao3':            
        novo_parametro = request.POST['valor_fb']
        parametros.f_min_bigramas = int(novo_parametro)
        parametros.save() 
    
    if opcao == 'opcao5':            
        novo_parametro = request.POST['valor_ae']
        parametros.acuidade = int(novo_parametro)
        parametros.save()

    if opcao == 'opcao4':
        return render(request, 'extrator/extrator_resultados.html', {'valorae':parametros.acuidade, 'valork':parametros.k_betweenness, 'valordelta':parametros.dr_delta_min, 'valorfc':parametros.f_corte, 'valorfb':parametros.f_min_bigramas,'goto':'ajuste'})

    
  
    return render(request, 'extrator/extrator_resultados.html', {'valorae':parametros.acuidade, 'valork':parametros.k_betweenness, 'valordelta':parametros.dr_delta_min, 'valorfc':parametros.f_corte, 'valorfb':parametros.f_min_bigramas,'goto':'ajuste'})      

def resultados(request,arquivo):
    result = DadosPreproc.objects.get(id=1)
    saco = 1   
    if saco == 1: #pura preguiça de tirar a identacao        
        temas = TemasNew.objects.all().values_list('tema', flat=True)
        tabela_graus_n = TabelaRanking.objects.all().values_list('vertice_nome','grau_norm')
        
        #paramentros genericos (raios)
        #raio do esfera parágrafo (deve ser igual ao definido no css)
        raio_par = 15 
        
        #Define o raio da menor esfera dos subtemas
        menor_grau = 1        
        for i in xrange(1, len(temas)):
            tema = TabelaRanking.objects.get(vertice_nome__exact=temas[i])            
            #menor grau
            if tema.grau_norm < menor_grau:
                menor_grau = tema.grau_norm         
        raio_vertices = float(20/menor_grau)

        #caclula parmetros do tema central - raio e diâmetro 
        irt_central = TemasNew.objects.get(tema__exact=temas[0])
        diametro_central = int(raio_vertices*irt_central.irt)
        raio_central = int(diametro_central/2)
        tema_central = (temas[0], diametro_central, raio_central,irt_central.irt_p)
        
        #calcula parametros dos parágrafos do tema central
        tema_central_par = []
        paragrafos = DadosExtracaoNew.objects.filter(tema__exact=temas[0])
        delta = int(180/len(paragrafos))
        posicao = 0
        
        #acha maior distancia entre tema central e parágrafo        
        bias_central = 0        
        for paragrafo in paragrafos:
            if paragrafo.protofrase.strip() != 'tema nao convergiu':
                distancia = int(tema_central[2] + raio_par + 80*(1-paragrafo.irse))             
                if distancia > bias_central:
                    bias_central = distancia
                pos_x = int(distancia*math.cos(math.radians(posicao)))
                pos_y = int(distancia*math.sin(math.radians(posicao)))
                posicao = posicao + delta
                nome = (temas[0] + str(pos_x) + str(pos_y))
                tema_central_par.append((temas[0], pos_x, pos_y, paragrafo.sentenca, nome, paragrafo.irse_p ))   
        
        # CALCULO DO BIAS ###############################################################################
        #acha maior distancia entre subtema e paragrafo (bias_subtema)
        bias_subtema = 0
        vet_buf = []
        for i in xrange(1, len(temas)):            
            #calcula parametros
            tema = TabelaRanking.objects.get(vertice_nome__exact=temas[i])
            irt = TemasNew.objects.get(tema__exact=temas[i])
            diametro_vertice = int(raio_vertices*irt.irt)
            raio_vertice = int(diametro_vertice/2)
            vet_buf.append((temas[i],raio_vertice))        
        
        for tema in temas:
            paragrafos = DadosExtracaoNew.objects.filter(tema__exact=tema)       
            for paragrafo in paragrafos:
                if paragrafo.protofrase.strip() != 'tema nao convergiu':
                    distancia = 0
                    for vetor in vet_buf:
                        if vetor[0] == tema:
                            distancia = int(vetor[1] + raio_par + 80*(1-paragrafo.irse))
                            if distancia > bias_subtema:
                                bias_subtema = distancia

        bias = bias_central + bias_subtema
        if not paragrafos:
            bias = 100             
        ##########################################################################################
        
        
        
        
        #Define os angulos dos temas e inicializa vetor
        delta_grau = float(360/(len(temas) - 1))    
        grau = delta_grau
        vetor_temas =[]   
        
        #menor raio
        t = TemasNew.objects.all()
        diametro_2_vertice = int(raio_vertices*t[1].irt)
        raio_2_vertice = int(diametro_2_vertice/2)
        menor_distancia_do_tema = raio_central + raio_2_vertice + bias + 10
        tem = TabelaRanking.objects.get(vertice_nome__exact=t[1].tema)
        distancia_do_centro = int(menor_distancia_do_tema/(1 - tem.grau_norm)) 
        
        for i in xrange(1, len(temas)):
            
            #calcula parametros
            tema = TabelaRanking.objects.get(vertice_nome__exact=temas[i])
            irt = TemasNew.objects.get(tema__exact=temas[i])
            diametro_vertice = int(raio_vertices*irt.irt)
            raio_vertice = int(diametro_vertice/2)
            distancia_centro = distancia_do_centro*(1 - tema.grau_norm)
            pos_x = int(distancia_centro*math.cos(math.radians(grau)))
            pos_y = int(distancia_centro*math.sin(math.radians(grau)))              

            #carrega vetor      
            vetor_temas.append((temas[i], distancia_centro ,pos_x, pos_y, diametro_vertice, raio_vertice, irt.irt_p ))
            grau = grau + delta_grau

        
        #maior posição de y (para valores negativos)   
        maior_distancia = 0
        for v in vetor_temas:
            if v[2] < maior_distancia:
                maior_distancia = v[2]
            
        maior_distancia = int(math.fabs(maior_distancia)) + 100

        #parêmetro de definição do tamanho dos vertices
        
        #define parametros dos paragrafos
        vetor_paragrafos = []
        
        for tema in temas:
            paragrafos = DadosExtracaoNew.objects.filter(tema__exact=tema)        
            delta = int(180/len(paragrafos))
            posicao = 0
            for paragrafo in paragrafos:
                if paragrafo.protofrase.strip() != 'tema nao convergiu':
                    distancia = 0
                    for vetor in vetor_temas:
                        if vetor[0] == tema:
                            distancia = int(vetor[5] + raio_par + 80*(1-paragrafo.irse))                                      
                    pos_x = int(distancia*math.cos(math.radians(posicao)))
                    pos_y = int(distancia*math.sin(math.radians(posicao)))
                    posicao = posicao + delta
                    nome = (tema + str(pos_x) + str(pos_y))                    
                    vetor_paragrafos.append((tema, pos_x, pos_y, paragrafo.sentenca, nome, paragrafo.irse_p  ))    
            
             
        #montagem da linha de extração
        cont = 0
        paragrafos_obj = DadosExtracaoNew.objects.all().values_list('sentenca','irgs_p').order_by('-irgs_p').distinct()
        paragrafos_linha = []
        for p in paragrafos_obj:
            if p[0].strip() != 'null - nao convergiu':
                nome = str(cont) + '_' + str(int(p[1]))
                paragrafos_linha.append((p[0].strip(),int(p[1]), int(100 - p[1]),nome))    
                cont += 1   
       
        #define a altura dos vertices na linha
        maior_top = 0
        paragrafos_linha_corrigido = []   
        irgs_count = Counter(elem[2] for elem in paragrafos_linha)
        for k,v in irgs_count.items():
            top = 0
            for p in paragrafos_linha:                
                if p[2] == k:
                    paragrafos_linha_corrigido.append((p[0],p[1],p[2],p[3],top))
                    top = top + 40
                    if top > maior_top:
                        maior_top = top
       
        if arquivo == 'fig1':           
            image = Image.open("extrator/arquivos/p4_grafico_alphas.png")
            image.show()           
            return render(request, 'extrator/extrator_resultados.html', {'top':maior_top , 'vetor_temas':vetor_temas, 'temas':temas, 'tema_central':tema_central,'vetor_paragrafos':vetor_paragrafos,'tema_central_par': tema_central_par,'maior_distancia':maior_distancia, 'altura':2*maior_distancia,'paragrafos_linha':paragrafos_linha_corrigido, 'posicao_linha': int(maior_distancia/2), 'mostra_res':'mostra_res', 'goto':'dados'})

        if arquivo == 'fig2':
            image = Image.open("extrator/arquivos/p4_grafico_alpha_selecionado.png")
            image.show() 
            return render(request, 'extrator/extrator_resultados.html', {'top':maior_top ,'vetor_temas':vetor_temas, 'temas':temas, 'tema_central':tema_central,'vetor_paragrafos':vetor_paragrafos,'tema_central_par': tema_central_par,'maior_distancia':maior_distancia, 'altura':2*maior_distancia,'paragrafos_linha':paragrafos_linha_corrigido, 'posicao_linha': int(maior_distancia/2), 'mostra_res':'mostra_res', 'goto':'dados'})

        if arquivo == 'fig3':
            image = Image.open("extrator/arquivos/p4_grafico_distancias_relativas_potenciacao.png")
            image.show() 
            return render(request, 'extrator/extrator_resultados.html', {'top':maior_top ,'vetor_temas':vetor_temas, 'temas':temas, 'tema_central':tema_central,'vetor_paragrafos':vetor_paragrafos,'tema_central_par': tema_central_par,'maior_distancia':maior_distancia, 'altura':2*maior_distancia,'paragrafos_linha':paragrafos_linha_corrigido, 'posicao_linha': int(maior_distancia/2), 'mostra_res':'mostra_res', 'goto':'dados'})
     
        if arquivo != 'none':
            #Abre arquivo no notepad++    
            programName = "C:/Program Files/Notepad++/notepad++.exe"
            fileName = "extrator/arquivos/" + arquivo + '.txt'
            subprocess.Popen([programName, fileName])
            return render(request, 'extrator/extrator_resultados.html', {'top':maior_top ,'vetor_temas':vetor_temas, 'temas':temas, 'tema_central':tema_central,'vetor_paragrafos':vetor_paragrafos,'tema_central_par': tema_central_par,'maior_distancia':maior_distancia, 'altura':2*maior_distancia,'paragrafos_linha':paragrafos_linha_corrigido, 'posicao_linha': int(maior_distancia/2), 'mostra_res':'mostra_res', 'goto':'dados'})
    
    return render(request, 'extrator/extrator_resultados.html', {'top':maior_top ,'vetor_temas':vetor_temas, 'temas':temas, 'tema_central':tema_central,'vetor_paragrafos':vetor_paragrafos,'tema_central_par': tema_central_par,'maior_distancia':maior_distancia, 'altura':2*maior_distancia,'paragrafos_linha':paragrafos_linha_corrigido, 'posicao_linha': int(maior_distancia/2), 'mostra_res':'mostra_res', 'goto':'resultados'})

def executar_passos_2_a_5(request):
    
    #carrega flags de execução
    r = DadosPreproc.objects.get(id=1)
    r.flag_completo = 'sim'
    r.save()
    
    #inicializa tempo
    inicio = time.time() 
    
    if r.flag_testapalavra == 'nao':
        #passo 2
        print 'Passo 1:'
        print 'executando o pré-processamento...'
        pre_processamento(request)
        print 'lematizando dados...'
        lematizar(request)
        print 'eliminando stop-words...'    
        eliminar_stopwords(request)
        print 'salvando dados...'
        salvar_dados(request)
        gerar_relatorio(request)
    
        #passo 22   
        print 'Passo 2'
        print 'separando os vértices da rede...'
        lista_de_vertices(request)
        print 'criando bigramas e lista de adjacências...'
        mapear(request)
        print 'gerando rede complexa dos dados...'
        matriz(request)
 
        #passo 4
        print 'Passo 4'
        print 'calculando métricas e rankeando os vértices...'
        metricas_e_ranking(request)
        print 'calculando índice de potenciação dos vértices...'  
        calcula_indice(request)   
    
    print 'selecionando os temas...'
    p = selecionar_temas(request)
    
    if p != 'none':
        return render(request, 'extrator/extrator_resultados.html', {'testa_sub':'sim' , 'palavra_candidata':p}) 

    #sai do modo testa substantivo
    r.testapalavra = 'nao'
    r.save()
    
    #passo 5 
    print 'Passo 5'
    print 'gerando as proto-frases...'
    processarProtofrases(request)
    print 'extraindo parágrafos...'
    mapearEextrair(request)
    print 'calculando índice de representatividade dos parágrafos extraídos...'
    calcula_indice_representatividade(request)
    print 'gerando resultados'
    resultados(request,'none')     
    
    r.flag_completo = 'nao'
    r.save()

    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))

    return render(request, 'extrator/extrator_resultados.html', {'tempo_p2a5':tempo_total,'mostra_res':'mostra_res'})