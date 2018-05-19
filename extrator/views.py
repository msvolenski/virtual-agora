# -*- coding: utf-8 -*-
from __future__ import division
from .models import SentencasGlobais, SentencasNucleos, SentencasExtraidas, MapasTemasESubtemas, Clusters, CorrigePalavra, ParametrosDeAjuste, TextoPreproc, ListaDeSubstantivos, TestaPalavra, DadosPreproc, ListaVertices, TabelaRanking, ListaDeAdjacencias, TemasNew, SentencasAvaliadas
from collections import OrderedDict, Counter
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from math import log
from nltk.tokenize import TweetTokenizer
from PIL import Image
from summa import keywords
from sklearn.neighbors.kde import KernelDensity
from numpy import array, linspace
from sklearn.cluster import KMeans
from itertools import groupby
from operator import itemgetter, attrgetter
from networkx.drawing.layout import kamada_kawai_layout
from django.conf import settings as djangoSettings
from django.db.models import Count
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
import itertools
import community
import igraph
import textwrap

class GraphTestView(generic.ListView):
  template_name = 'extrator/graph_test.html'
  #model = Topic
  def get_queryset(self):
     #u = User.objects.get(user=self.request.user)
     return #Topic.objects.filter(published='Sim',projeto__sigla=u.user.user.projeto).distinct()

class ResultadosExtratorHomeView(generic.ListView):
  template_name = 'extrator/extrator_resultados.html'
  
  def get_queryset(self):
    return  
  

############################################  PASSO 1 #################################################################################################################################

def inserir_dados_de_entrada(request):
    #CRIA/lÊ O ARQUIVO ONDE SERÁ INSERIDO OS DADOS DE ENTRADA
    
    if os.path.exists("extrator/arquivos/p1_texto_inicial_original.txt"):
            programName = "C:/Program Files/Notepad++/notepad++.exe"
            fileName = "extrator/arquivos/p1_texto_inicial_original.txt"
            subprocess.Popen([programName, fileName])
            dados_de_entrada = codecs.open("extrator/arquivos/p1_texto_inicial_original.txt","r","utf-8").read()         
            return render(request, 'extrator/extrator_resultados.html', {'goto':'passo1','muda_logo':'logo_vis_dados'})
    else:
        file_doc_original = codesc.open("extrator/arquivos/p1_texto_inicial_original.txt","w","utf-8")
        file_doc_original.close()
        programName = "C:/Program Files/Notepad++/notepad++.exe"
        fileName = "extrator/arquivos/p1_texto_inicial_original.txt"
        subprocess.Popen([programName, fileName])
        dados_de_entrada = codecs.open("extrator/arquivos/p1_texto_inicial_original.txt","r","utf-8").read()        
        
        return render(request, 'extrator/extrator_resultados.html', {'goto':'passo1','muda_logo':'logo_vis_dados'})


def inserir_dados_de_entrada_twitter(request):
   
    #carrega parametros de ajuste
    try:
        parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
        
    except ObjectDoesNotExist:
        parametros = ParametrosDeAjuste(ident=1,k_betweenness=100,f_corte=10,f_min_bigramas=50,num_tweets=100)
        parametros.save()
    
    #define documento de entrada
    entrada_tweets_copia = codecs.open("extrator/arquivos/p1_texto_inicial_original.txt","w", "utf-8")
    
    #busca palavra digita e testa sua existencia
    hashtags = request.POST['hashtag']
    hashtag_list = hashtags.split(' ')    
    
    if not hashtags:        
        return render(request, 'extrator/extrator_home.html', {'dados_de_entrada': None})

    #busca dados no twitter
    consumer_key = 'NfaYz4Enkx2V2tOsjCv2lSiyr'
    consumer_secret = 'jwGB1ppEFsMkYldOSszCAE1j6paib0IolFn02dBQJM5g1u5AvQ'
    access_token = '493595634-6Qv9H8bBkRJ8FHme6yHu3HW4BUmVHLjYXXqWqOic'
    access_token_secret = '7bxNoz9El5H9w2Af0jx3pXiWvQuiBCggkoFwmQHkeuYRt'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)    
    api = tweepy.API(auth)    

    for hashtag in hashtag_list:
        print "Tweets para " + hashtag
        #variaveis
        num_tweets = parametros.num_tweets
        contador_tweets = 0
        max_id = 0
        permitir_RT = parametros.permitir_RT
        fim = 'nao'
        
        #primeira Busca - Define o ultimo_id
        public_tweets = api.search(q=hashtag ,lang='pt', count=100, result_type='recent')
        ultimo_id = public_tweets[-1].id
        
        #salva primeiros tweets
        for tweet in public_tweets:          
            if permitir_RT == 'sim':            
                if hasattr(tweet, 'retweeted_status'):
                    if contador_tweets < num_tweets:
                        if not tweet.retweeted_status.truncated:
                            entrada_tweets_copia.write(tweet.retweeted_status.text)
                            entrada_tweets_copia.write('.')                                          
                            entrada_tweets_copia.write('\n\n')
                            contador_tweets += 1                    
                    else:
                        fim = 'sim'               
                else:
                    if contador_tweets < num_tweets:
                        if not tweet.truncated:
                            entrada_tweets_copia.write(tweet.text)
                            entrada_tweets_copia.write('.')                                            
                            entrada_tweets_copia.write('\n\n')
                            contador_tweets += 1                    
                    else:
                        fim = 'sim'
            
            if permitir_RT == 'nao':
                if hasattr(tweet, 'retweeted_status'):
                    do = 'nothing'
                else:            
                    if contador_tweets < num_tweets:
                        if not tweet.truncated:
                            entrada_tweets_copia.write(tweet.text)
                            entrada_tweets_copia.write('.')                                            
                            entrada_tweets_copia.write('\n\n')
                            contador_tweets += 1                    
                    else:
                        fim = 'sim'            
        
        print str(contador_tweets) + " Tweets carregados..." 
        
        while fim == 'nao':       
            public_tweets = api.search(q=hashtag ,lang='pt', count=100, max_id=(ultimo_id - 1) , truncated='false')   
            for tweet in public_tweets:          
                if permitir_RT == 'sim':
                    if hasattr(tweet, 'retweeted_status'):                    
                        if contador_tweets < num_tweets:
                            if not tweet.retweeted_status.truncated:
                                entrada_tweets_copia.write(tweet.retweeted_status.text)
                                entrada_tweets_copia.write('.')                                        
                                entrada_tweets_copia.write('\n\n')
                                contador_tweets += 1                        
                        else:
                            fim = 'sim'               
                    else:
                        if contador_tweets < num_tweets:
                            if not tweet.truncated:
                                entrada_tweets_copia.write(tweet.text)
                                entrada_tweets_copia.write('.')                                               
                                entrada_tweets_copia.write('\n\n')
                                contador_tweets += 1                        
                        else:
                            fim = 'sim'
            
                if permitir_RT == 'nao':
                    if hasattr(tweet, 'retweeted_status'):  
                        do = 'nothing'
                    else:            
                        if contador_tweets < num_tweets:
                            if not tweet.truncated:
                                entrada_tweets_copia.write(tweet.text) 
                                entrada_tweets_copia.write('.')                       
                                entrada_tweets_copia.write('\n\n')
                                contador_tweets += 1
                            
                        else:
                            fim = 'sim'     

            print str(contador_tweets) + " Tweets carregados..."      
            
            try:
                ultimo_id = public_tweets[-1].id    
            except:
                fim = 'sim'    
    
    entrada_tweets_copia.close() 

    return render(request, 'extrator/extrator_resultados.html', {'contador_nt':contador_tweets, 'goto':'passo1','muda_logo':'logo_twitter'})


def salvar_dados_iniciais(request):
    print "Salvando dados..."  
    
    #Separa tokens para processamento do documento
    entrada_original = codecs.open("extrator/arquivos/p1_texto_inicial_original.txt","r", "utf-8")
    entrada_tokenizada1 = codecs.open("extrator/arquivos/p1_texto_inicial_tokens.txt","w", "utf-8")
    entrada_tokenizada2 = codecs.open("extrator/arquivos/p2_texto_inicial_tokens_corrigido.txt","w", "utf-8")

    #grava tokens nos novos arquivos  
    documento = entrada_original.read()
    documento_or = documento
    
    #resolve problema dos links do twiiter
    documento = re.sub(r"http\S+", ".", documento)    

    #elimina os mais ainda malditos emoticons e outros caracteres 
    myre = re.compile('('
            '\x96|' #caractere bizarro SPA 
            '\u200b|' #MALDITO ESPAO BRANCO
            '[\ud800-\udbff][\udc00-\udfff]|'
            '\ud83c[\udf00-\udfff]|'
            '\ud83d[\udc00-\ude4f\ude80-\udeff]|'
            '\ud83e[\u0000-\uffff]|'
            '[\u2600-\u26FF\u2700-\u27BF])+'.decode('unicode_escape'), 
            re.UNICODE)            
    documento = myre.sub('',documento)      
   
    #tokenizer para Tweets
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
    palavras = tknzr.tokenize(documento)    
      
    for token in palavras: 
            
        #substitui as risadas
        token = re.sub(r'\b([kK]+)\b', 'k', token)
        token = re.sub(r'\b([aA]+)\b', 'a', token)
        token = re.sub(r'(rs)+', 'rs', token)
        token = re.sub(r'\b[ha|HA|hA|Ha](ha|hA|Ha|HA|ah|Ah|AH|a|h|A|H)+\b', 'ha', token)
        token = re.sub(r'\b[he|HE|hE|He](he|hE|He|HE|eh|Eh|EH|e|h|E|H)+\b', 'he', token)
        token = re.sub(r'\b[hi|HI|hI|Hi](hi|hI|Hi|HI|ih|Ih|IH|i|h|I|H)+\b', 'hi', token)
        
        #elimina repetições exessivas de vogais
        token = re.sub(r'aa[a]?', 'a', token)
        token = re.sub(r'ee[e]?', 'e', token)
        token = re.sub(r'ii[i]?', 'i', token)
        token = re.sub(r'oo[o]?', 'o', token)
        token = re.sub(r'uu[u]?', 'u', token)
        test = re.match(r'(.*?(\n))+.*?', token)
        if test:
            token = '.'

        entrada_tokenizada1.write(token.rstrip())
        try:
            correta = CorrigePalavra.objects.get(palavra=token.rstrip()) 
            entrada_tokenizada2.write(correta.palavra_correta.rstrip())
        except:
            entrada_tokenizada2.write(token.rstrip())
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
        DadosPreproc.objects.create(id=1, corretor='off')
     
    return render(request, 'extrator/extrator_resultados.html', {'documento':documento_or,'goto':'resultado-passo-1','muda_logo':'logo_salvar_dados'})


def corretor_ortografico(request):   
      
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
             
        #para a Biblia: testa se primeira palavra é maiúsculo
        flag_nomeproprio = 'nao'
        padrao = re.compile("^[ABCDEFGHIJKLMNOPQRSTUVWYZ]")
        eh_nomeproprio = padrao.match(palavra)
        if eh_nomeproprio:
            flag_nomeproprio = 'sim' 
        
        #testa se a palavra é um número
        flag_numero = 'nao'
        padrao = re.compile("[0-9]+")
        eh_numero = padrao.match(palavra)
        if eh_numero:
            flag_numero = 'sim'        
        
        #Testa se o token é uma palavra (formada por letras)
        pattern = re.compile("(?:[.A-Za-z0-9áãõÃÕéóíúàèìòùêâîôûÂÊÎÔÛÁÉÍÓÚÀÈÌÒÙÇç-]+)$")        
        eh_palavra = pattern.match(palavra.encode('utf-8'))                
            
        if eh_palavra:
            #testa se a palavra está no dicionario        
            res = corretor.check(palavra.encode("iso-8859-1"))

            #condição caso a palavra nao estiver no dicionário                
            if res == 0 and palavra not in palavras_ignoradas and flag_numero == 'nao' and flag_nomeproprio == 'nao': 
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
    
    return render(request, 'extrator/extrator_resultados.html', {'goto':'passo1','muda_logo':'logo_corretor'})


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

        #cria novo objeto CorrigePalavra
        novo = CorrigePalavra(palavra=palavras[int(posicao)], palavra_correta=palavra_correta)
        novo.save() 

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
            
            #cria novo objeto CorrigePalavra
            novo = CorrigePalavra(palavra=palavras[int(posicao)], palavra_correta=palavra_correta)
            novo.save()

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
    
    if opcao == 'opcao5':
        return render(request, 'extrator/extrator_resultados.html', {'goto':'passo1'})        
    
    return render(request, 'extrator/extrator_resultados.html', {'goto':'passo1'})


######### FIM PASSO 1 ################################################################################################################################################################




########### PASSO 2 #############################################################################################################################################################################

def pre_processamento(request):
    print "Preparando dados..."
   
    #Tokeniza o texto e escreve em documento único.
    arq_texto_preproc = codecs.open('extrator/arquivos/p2_texto_preprocessado.txt','w','utf-8')
    arq_texto_preproc_vet = file_org = codecs.open("extrator/arquivos/p2_texto_preprocessado_vetorizado.txt","w",'utf-8')
    arq_texto_inicial = codecs.open("extrator/arquivos/p2_texto_inicial_tokens_corrigido.txt", "r", "utf-8")
    texto_inicial = arq_texto_inicial.read()
    lista_palavras = []  

    #elimina pontuação repetida
    texto_inicial = re.sub(r'[\?\.\!\;]+(?=[\?\.\!\;])', '', texto_inicial)
    
    #substitui pontuação por ponto final
    texto_inicial = re.sub(r'[!|?|;|.|:|\[|\]]', '.', texto_inicial)
   
    #Separa os tokens
    #tokenizer para Tweets
    tknzr = TweetTokenizer()
    tokens = tknzr.tokenize(texto_inicial)      
    
    #conta número de palavras
    contador = 0
    flag = 'ok'
    for token in tokens:
        pattern = re.compile("(?:[A-Za-z0-9áãõÃÕéóíúàèìòùêâîôûÂÊÎÔÛÁÉÍÓÚÀÈÌÒÙÇç-]+)$") #considera palavra os tokens que contém uma combinação destes caracteres       
        eh_palavra = pattern.match(token.encode('utf-8'))
        if eh_palavra:
            contador = contador + 1     
    
    #Conta o número de sentenças e escreve tokens nos arquivos e substitui pontuação
    sentencas = 0
    for item in tokens:        
        pat = re.compile("[\:\;\.\!\?\-\]\[]+")
        eh = pat.match(item)        
        if eh:
            item = "."
            sentencas = sentencas + 1
        item_l = item.lower()
        
        #1. procura por pontos no meio da palavra char-.-char
        pattern = re.compile(ur"\D+\.\D+")
        eh_palavra = pattern.match(item_l)
        if eh_palavra:                     
            p =[]
            print item_l
            for i in item_l:
                if i != '.':
                    p.append(i)    
            item_l = ''.join(p)  
            print item_l

        #procura por pontos no meio da palavra digito-.-char
        pattern = re.compile(ur"\d+\.\D+")
        eh_palavra = pattern.match(item_l)        

        if eh_palavra:
            f = 'nachou'
            p =[]          
            for i in item_l:
                if f == 'achou':
                    p.append(i)
                if i == '.':
                    f = 'achou'
            item_l = ''.join(p)   
        
        #elimina todo item que tem o ... do twitter substituindo por um ponto final
        pattern = re.compile(ur'.*…')
        eh_palavra = pattern.match(item_l)
        if eh_palavra:
            item_l = '.'         
        if item_l:
            try:
                item_l.encode('utf-8')
            except UnicodeError:
                flag = 'error'
                print 'Erro de codificacao: ' + repr(item_l)
            if flag == 'ok':
                lista_palavras.append(item_l.rstrip())
                flag = 'ok'
            flag = 'ok'
    
    #elimina ultima espaço em branco
    #lista_palavras.pop(-1)

    #armazena nos arquivos
    arq_texto_preproc.write(' '.join(lista_palavras).rstrip())
    arq_texto_preproc_vet.write('\n'.join(lista_palavras).rstrip())    

    arq_texto_preproc.close()
    arq_texto_preproc_vet.close()
    arq_texto_inicial.close()

    #Salva dados no Banco de dados   
    dados_preprocessamento = DadosPreproc.objects.get(id=1)
    dados_preprocessamento.quantidade_de_sentencas = sentencas
    dados_preprocessamento.palavras_texto_original = str(contador)
    dados_preprocessamento.save()
       
    return render(request, 'extrator/extrator_resultados.html', {'muda_logo':'logo_preparar_dados','goto':'passo2'})


def lematizar(request):
    print "Lematizando dados..."
    
    #inicializa listas
    lista_palavras = []
    
    #Abre o Bash e executa o lematizador no texto inicial
    is32bit = (platform.architecture()[0] == '32bit')
    system32 = os.path.join(os.environ['SystemRoot'],
                        'SysNative' if is32bit else 'System32')
    bash = os.path.join(system32, 'bash.exe')
    start_time = time.time()
    p = subprocess.check_call('"%s" -c "cd Linguakit-master ; ./linguakit lem pt ../extrator/arquivos/p2_texto_preprocessado.txt > ../extrator/arquivos/p2_saida_lematizador.txt ; unix2dos ../extrator/arquivos/p2_saida_lematizador.txt"' % bash, shell=True)
    temp =  time.time() - start_time
    
    #abre o texto já lematizado e cria dois novos arquivos: um com o texto original e outro com o texto lematizado
    saida_lematizador = codecs.open("extrator/arquivos/p2_saida_lematizador.txt","r","utf-8")
    texto_lematizado = codecs.open("extrator/arquivos/p2_texto_lematizado.txt","w",'utf-8')
    texto_lematizado_vetor = codecs.open("extrator/arquivos/p2_texto_lematizado_vetor.txt","w",'utf-8')
    
    #Pega a palavra lematizada no documento de saída do lematizador
    contador = 0
    for linha in saida_lematizador:
        if linha:
        #if linha != "\n":                 
            try:           
                linha.split(' ')[2]
                if linha[0] != ' ':    
                    word_lem = linha.rstrip().split(' ')[1]
                    if word_lem:
                        lista_palavras.append(word_lem)
                   
                    
                    #contador de palavras
                    pattern = re.compile("(?:[A-Za-z0-9áãõÃÕéóíúàèìòùêâîôûÂÊÎÔÛÁÉÍÓÚÀÈÌÒÙÇç-]+)$") #considera palavra os tokens que contém uma combinação destes caracteres       
                    eh_palavra = pattern.match(word_lem.encode('utf-8'))
                    if eh_palavra:
                        contador = contador + 1 
        
            except:
                if linha[0] != ' ':    
                    word_lem = linha.rstrip().split(' ')[0]           
                    if word_lem:
                        lista_palavras.append(word_lem)
                
                    #contador de palavras
                    pattern = re.compile("(?:[A-Za-z0-9áãõÃÕéóíúàèìòùêâîôûÂÊÎÔÛÁÉÍÓÚÀÈÌÒÙÇç-]+)$") #considera palavra os tokens que contém uma combinação destes caracteres       
                    eh_palavra = pattern.match(word_lem.encode('utf-8'))
                    if eh_palavra:
                        contador = contador + 1
    
    #armazena nos arquivos
    texto_lematizado.write(' '.join(lista_palavras).rstrip())
    texto_lematizado_vetor.write('\n'.join(lista_palavras).rstrip())    
    
    texto_lematizado_vetor.close()
    texto_lematizado.close()
    
    #Salva quantidade de palavras no banco de dados    
    dados_preprocessamento = DadosPreproc.objects.get(id=1)
    dados_preprocessamento.palavras_texto_lematizado = str(contador)
    dados_preprocessamento.save()  
   
    return render(request, 'extrator/extrator_resultados.html', {'goto': 'passo2', 'muda_logo':'logo_lematizar'})    


def eliminar_stopwords(request):
    print "Eliminando Stop-Words..."

    #Lê arquivo de stop-words e cria uma lista
    if os.path.exists("extrator/arquivos/p2_lista_stopwords.txt"):
        arq_stopwords = codecs.open("extrator/arquivos/p2_lista_stopwords.txt", "r", "utf-8")
        lista_de_stopwords = arq_stopwords.readlines()        
    else:        
        return render(request, 'extrator/extrator_home_2.html', {})
    
    stopwords = []
    lista_palavras =[]
    for linha in lista_de_stopwords:
        stopwords.append(linha.strip())
    
    #lê texto lematizado
    arq_texto = codecs.open("extrator/arquivos/p2_texto_lematizado.txt", "r", "utf-8")
    texto = arq_texto.read()
    palavras = texto.rstrip().split(' ')
    
    #gera arquivos de saída
    arq_saida = codecs.open("extrator/arquivos/p2_texto_lematizado_ssw.txt","w", "utf-8")
    arq_saida_vetor = codecs.open("extrator/arquivos/p2_texto_lematizado_ssw_vetor.txt","w", "utf-8")
    
    #verifica se a palavra é uma stop-word, grava palavras no arquvivo e conta número de palavras
    contador = 0
    cont_idx = 0
    for palavra in palavras:    
        if palavra.strip() not in stopwords:
            lista_palavras.append(palavra.rstrip())            
            
            #contador de palavras
            pattern = re.compile("(?:[A-Za-z0-9áãõÃÕéóíúàèìòùêâîôûÂÊÎÔÛÁÉÍÓÚÀÈÌÒÙÇç-]+)$") #considera palavra os tokens que contém uma combinação destes caracteres       
            eh_palavra = pattern.match(palavra.encode('utf-8'))
            if eh_palavra:
                contador = contador + 1 
    
    #armazena nos arquivos
    arq_saida.write(' '.join(lista_palavras).rstrip())
    arq_saida_vetor.write('\n'.join(lista_palavras).rstrip())  
    
    arq_saida.close()
    arq_saida_vetor.close() 

    #Salva quantidade de palavras do texto SSW no BD    
    dados_preprocessamento = DadosPreproc.objects.get(id=1)
    dados_preprocessamento.palavras_texto_lematizado_ssw = str(contador)
    dados_preprocessamento.save()     
    
    return render(request, 'extrator/extrator_resultados.html', {'goto':'passo2','muda_logo':'logo_eliminar_sw'  })    


def salvar_dados(request):
    print "Salvando dados procesados..."
       
    #Pega objetos-texto e reinicializa o BD para receber novo texto
    texto_passo1 = TextoPreproc.objects.all()
    texto_passo1.delete()   
    
    #salvando via bulk
    tokens = codecs.open("extrator/arquivos/p2_texto_lematizado_ssw_vetor.txt", "r", "utf-8").readlines()
    
    #elimina espaçoes em brannco
    tokens_list = []
    tokens = filter(None, tokens)
    for t in tokens:        
        tokens_list.append(t.strip())    
    tokens_list = filter(None, tokens_list)        
    aList = [TextoPreproc(vertice=token, vertice_num=-1) for token in tokens_list]    
    TextoPreproc.objects.bulk_create(aList)
   
    return render(request, 'extrator/extrator_resultados.html', {'goto': 'passo2','muda_logo':'logo_salvar_bd' })


def gerar_relatorio(request):
    print "Gerando relatorio Passo 2..."
   
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

    return render(request, 'extrator/extrator_resultados.html', {'documento_p2':p2_relatorio,'goto': 'resultado-passo-2','muda_logo':'logo_gerar_rp2'})

def executa_passo_2(request):
    
    pre_processamento(request)
    lematizar(request)
    eliminar_stopwords(request)
    salvar_dados(request)
    gerar_relatorio(request)
    
    #LÊ relatório    
    p2_relatorio = codecs.open("extrator/arquivos/p2_relatorio.txt","r","utf-8").read()
    
    return render(request, 'extrator/extrator_resultados.html', {'documento_p2':p2_relatorio,'goto': 'resultado-passo-2','muda_logo':'logo_gerar_rp2'})

######### FIM PASSO 2 ################################################################################################################################################################




########### PASSO 3 #############################################################################################################################################################################

def lista_de_vertices(request):
    print "Gerando Vertices da rede..."
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
            vertices[index] = item.strip()
            index = index + 1
    
    #Salva no BD via bulk    
    aList = [ListaVertices(index = key, node = element.strip()) for key,element in vertices.iteritems()]    
    ListaVertices.objects.bulk_create(aList) 
        
    return render(request, 'extrator/extrator_resultados.html', {'goto': 'passo3', 'muda_logo':'logo_def_vertices' })

def mapear(request):
    print "Indexando dados do documento..."
    #Objetivo: Associar cada palavra do texto lematizado ao seu respectivo indice

    #carrega objetos
    palavras = TextoPreproc.objects.all().values_list('vertice','vertice_num')    
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
    aList = [TextoPreproc(vertice=linha[0].rstrip(), vertice_num=linha[1]) for linha in lista_texto]    
    TextoPreproc.objects.bulk_create(aList)    
        
    return render(request, 'extrator/extrator_resultados.html', {'goto': 'passo3' , 'muda_logo':'logo_indexar'})


def matriz(request):
    print "Gerando lista de adjacencias..."        
    #Objetivo: gera a lista de adjacencias a partir de uma matriz de adjacências

    #Inicializa arquivos
    arq_listaAdjacencias = codecs.open("extrator/arquivos/p3_lista_adjacencias.txt","w",'utf-8')
    arq_subdocumento = codecs.open("extrator/arquivos/p3_texto_sentencas.txt",'w','utf-8')
    
    #lista
    lista_strings =[]
    
    #inicializa e carrega dados do BD
    ListaDeAdjacencias.objects.all().delete()  
    tokens = TextoPreproc.objects.all()
    
    #Gera documento de sentencas    
    string = ''
    for token in tokens:       
        if token.vertice == '.':            
            string = string.rstrip()            
            lista_strings.append(string.rstrip())
            string = ''
        else:
            string = string + token.vertice.rstrip() + ' '    
    
    arq_subdocumento.write('\n'.join(lista_strings).rstrip())   
    arq_subdocumento.close()   
   
    #lÊ documento de sentenças
    sentencas = codecs.open('extrator/arquivos/p3_texto_sentencas.txt','r','utf-8').read().splitlines()

    #cria lista de adjancecias
    lista_adjacencias = OrderedDict()
    for sentenca in sentencas:
        bigrama = 'ok'
        palavras_sentenca = sentenca.rstrip().split(' ')
        for i, palavra in enumerate(palavras_sentenca):
            try:                                            
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
       
    return render(request, 'extrator/extrator_resultados.html', {'goto':'passo3','muda_logo':'logo_rede'})


def rede_complexa(request):
    print "Gerando Rede Complexa dos dados..."        
    #Lê arquivo que contém a lista de adjacenicas
    arq_listaAdjacencias = codecs.open("C:/virtual-agora/extrator/arquivos/p3_lista_adjacencias.txt","r","utf-8")
    arq_json = codecs.open(djangoSettings.STATIC_ROOT + "\\agora\\json\\p3_json_rede.json", 'w', 'utf-8') 

    listaAdjacencias = arq_listaAdjacencias.readlines()

    #carrega lista de vertices
    lista_de_vertices_t = ListaVertices.objects.all()

    arq_json.write("{\n    \"nodes\": [\n        ")
    
    #gera rede
    rede = nx.DiGraph()
    
    #escreve os nós
    for i , vertice in enumerate(lista_de_vertices_t):
        idn = 1
        #arq_json.write("{\n            \"name\": \"" + vertice.node + "\",\n            \"label\": \"0\",\n            \"id\": \"" + str(vertice.index)+ "\"\n        }")      
        arq_json.write("{\n            \"id\": \"" + vertice.node + "\",\n            \"group\": \"0\",\n            \"other\": \"" + str(vertice.index)+ "\"\n        }")      

        if i == (len(lista_de_vertices_t) -1):
            arq_json.write("\n    ],\n    ")         
        else:
            arq_json.write(",\n        ")
        rede.add_node(vertice.node)
        idn = idn + 1
    #escreve os links
    arq_json.write("\"links\": [\n")         

    for i, bigrama in enumerate(listaAdjacencias):                
        vertice_inicial = bigrama.split(' ')[0]       
        vi_obj = ListaVertices.objects.get(node__exact=vertice_inicial)
        vi_index = vi_obj.index
        vertice_final = bigrama.split(' ')[1]
        vf_obj = ListaVertices.objects.get(node__exact=vertice_final)
        vf_index = vf_obj.index
        peso = float(bigrama.split(' ')[2])
        arq_json.write("        {\n            \"source\": \"" + vertice_inicial + "\",\n            \"target\": \"" + vertice_final + "\",\n            \"value\": " + str(int(peso)) + "\n        }" )         
        if i == (len(listaAdjacencias) -1):
            arq_json.write("\n    ]\n}")         
        else:
            arq_json.write(",\n")
        rede.add_edge(vertice_inicial, vertice_final, weight=peso)
        
    nx.write_gexf(rede, "extrator/p3_rede_complexa_gephi.gexf")           
    
    return render(request, 'extrator/extrator_resultados.html', {'muda_logo':'logo_mat','rede_p3':"rede",'goto': 'resultado-passo-3'})    


def executa_passo_3(request):
      
    lista_de_vertices(request)
    mapear(request)    
    matriz(request)
    rede_complexa(request)    
    
    return render(request, 'extrator/extrator_resultados.html', {'muda_logo':'logo_mat','rede_p3':"doc",'goto': 'resultado-passo-3'})    

######### FIM PASSO 3 ################################################################################################################################################################




########### PASSO 4 #############################################################################################################################################################################

def metricas_e_ranking(request): 
    print "Calculando metricas de centralidade..."
    #Objetivo: calcular as métricas de centralidade da rede e gerar tabelas    
    
    #carrega parametros de ajuste
    try:
        parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
        
    except ObjectDoesNotExist:
        parametros = ParametrosDeAjuste(ident=1,k_betweenness=100,f_corte=10,f_min_bigramas=50)
        parametros.save()

    #Lê arquivo que contém a lista de adjacenicas
    arq_listaAdjacencias = codecs.open("C:/virtual-agora/extrator/arquivos/p3_lista_adjacencias.txt","r","utf-8")
    listaAdjacencias = arq_listaAdjacencias.readlines()

    #Cria arquivos para receber as tabelas
    arq_tabela_graus = codecs.open("extrator/arquivos/p4_tabela_graus.txt", 'w', 'utf-8')
    arq_tabela_betweenness = codecs.open("extrator/arquivos/p4_tabela_betweenness.txt", 'w','utf-8')
    arq_tabela_eigenvector = codecs.open("extrator/arquivos/p4_tabela_eigenvector.txt", 'w','utf-8')
    arq_texto_vertices = codecs.open("extrator/arquivos/p4_aux_texto_vertices.txt", 'w','utf-8')

    #Prepara banco de dados para receber as tabelas
    tabelas = TabelaRanking.objects.all()
    tabelas.delete()

    #carrega lista de vertices
    lista_de_vertices = ListaVertices.objects.all()

    #cria tabelas
    tabela_graus = {}
    tabela_betweenness = {}
    tabela_eigenvector ={}

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
   
    #"calculando métrica graus...print"
    tabela_graus_t = nx.degree(rede, weight='weight')     
    tabela_graus = dict(tabela_graus_t)
    maior_grau = max(tabela_graus.iteritems(), key=operator.itemgetter(1))[1]
    
    # "calculando métrica betweenness..."
    tabela_betweenness = nx.betweenness_centrality(rede, weight='weight', normalized=False, k=int(float(parametros.k_betweenness/100)*len(rede.nodes())))    
    maior_betweenness = max(tabela_betweenness.iteritems(), key=operator.itemgetter(1))[1]
    
    #"calculando métrica eigenvector..."
    try:
        tabela_eigenvector = nx.eigenvector_centrality(rede)
    except:
        tabela_eigenvector = nx.eigenvector_centrality_numpy(rede)
    maior_eigenvector = max(tabela_eigenvector.iteritems(), key=operator.itemgetter(1))[1]
       
   
    #GERA REDE GEPHI  
    nx.write_gexf(rede, "extrator/arquivos/p3_rede_complexa_gephi.gexf")
  
    #cria lista de vertices
    vertices = nx.nodes(rede)

    #gera dicionarios de valores normalizados e cria um texto de vertices (para o próximo passo)
    tabela_grau_normalizado = {}
    tabela_betweenness_normalizado = {}
    tabela_eigenvector_normalizado = {}    
    
    #gera conteudo das tabelas
    for vertice in vertices:        
        arq_texto_vertices.write(vertice + ' ')       
        tabela_grau_normalizado[vertice] = tabela_graus.get(vertice)/maior_grau    
        tabela_betweenness_normalizado[vertice] = tabela_betweenness.get(vertice)/maior_betweenness    
        tabela_eigenvector_normalizado[vertice] = tabela_eigenvector.get(vertice)/maior_eigenvector   
    
    #Armazenando Tabelas no BD via Bulking 
    aList = [TabelaRanking(vertice_nome = vertice, vertice_numero=ListaVertices.objects.get(node__exact=vertice).index, grau=tabela_graus[vertice], grau_norm=tabela_grau_normalizado[vertice], 
        betweenness=tabela_betweenness[vertice], betweenness_norm=tabela_betweenness_normalizado[vertice], 
        eigenvector=tabela_eigenvector[vertice], eigenvector_norm=tabela_eigenvector_normalizado[vertice], potenciacao=1.0) for vertice in vertices]
    TabelaRanking.objects.bulk_create(aList)   
    
    #gera Tabelas Ranking
    tabela_graus_ordenada = TabelaRanking.objects.all().order_by('-grau')    
    tabela_betweenness_ordenada = TabelaRanking.objects.all().order_by('-betweenness')    
    tabela_eigenvector_ordenada = TabelaRanking.objects.all().order_by('-eigenvector')
    
    #Salva ranking graus em arquivo
    for linha in tabela_graus_ordenada:
        arq_tabela_graus.write(linha.vertice_nome + ' ' + str(linha.grau) + ' ' + str(linha.grau_norm) + '\n')
    
    #Salva ranking betweenness em arquivo
    for linha in tabela_betweenness_ordenada:
        arq_tabela_betweenness.write(linha.vertice_nome + ' ' + str(linha.betweenness) + ' ' + str(linha.betweenness_norm) + '\n')
    
    #Salva ranking eigenvector em arquivo
    for linha in tabela_eigenvector_ordenada:
        arq_tabela_eigenvector.write(linha.vertice_nome + ' ' + str(linha.eigenvector) + ' ' + str(linha.eigenvector_norm) + '\n') 

    #fecha arquivos
    arq_tabela_graus.close()
    arq_tabela_betweenness.close()
    arq_tabela_eigenvector.close()
    arq_texto_vertices.close()  
        
    return render(request, 'extrator/extrator_resultados.html', {'goto': 'passo4', 'muda_logo':'logo_calc_metricas' }) 


def calcula_indice(request):
    print "Calculando Indice de Potenciacao..."
        
    #OBJETIVO: definir a forma de calcular a potenciacao (seus pesos) e gerar a tabela potenciacao
        
    #Abre arquivo de dados a serem lidos
    tabela_grau = codecs.open("extrator/arquivos/p4_tabela_graus.txt").readlines()
    tabela_betweenness = codecs.open("extrator/arquivos/p4_tabela_betweenness.txt").readlines()
    tabela_eigenvector = codecs.open("extrator/arquivos/p4_tabela_eigenvector.txt").readlines()
    
    #Carrega dados do BD
    parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)    
    vertices_objs = ListaVertices.objects.all()
    tabela_ranking_completa = TabelaRanking.objects.all()
               
    #Inicializa arquivos a serem escritos
    arq_tabela_potenciacao = codecs.open("extrator/arquivos/p4_tabela_potenciacao.txt", 'w', 'utf-8')    
    
    #CALCULA POTENCIAÇÃO
    
    for vertice in vertices_objs:
        grau_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).grau_norm
        bet_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).betweenness_norm
        eigen_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).eigenvector_norm
        potenciacao = float(grau_n) + float(bet_n) + float(eigen_n)
             
    #   Salva na Tabela Ranking
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
 
    #fecha arquivo
    arq_tabela_potenciacao.close()
    
    return render(request, 'extrator/extrator_resultados.html', {'goto': 'passo4', 'muda_logo':'logo_calc_indice'})


def selecionar_temas(request):
    print "Selecionando os Temas..."
            
    #carrega dados
    r =  DadosPreproc.objects.get(id=1)
    tabela_bigramas = ListaDeAdjacencias.objects.all()
            
    #inicializa dados do BD
    TemasNew.objects.all().delete()    
    vertices_objs = ListaVertices.objects.all()
            
    #carrega parametros de ajuste
    try:
        parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
        
    except ObjectDoesNotExist:
        parametros = ParametrosDeAjuste(ident=1,k_betweenness=100,f_corte=10,f_min_bigramas=50,faixa_histo=0.1)
        parametros.save()
            
    #cria arquivo de tabela para histograma
    arq_tabela_histo = codecs.open("extrator/arquivos/p5_tabela_histograma.txt", 'w', 'utf-8')  
    arq_clusters = codecs.open("extrator/arquivos/p5_clusters.txt", 'w', 'utf-8') 
    arq_relatorio = codecs.open("extrator/arquivos/p5_relatorio_temas.txt", 'w')
    arq_json = codecs.open(djangoSettings.STATIC_ROOT + "\\agora\\json\\p4_json_histograma.json", 'w', 'utf-8') 

    #carrega tabela potenciação
    tabela_potenciacao = codecs.open("extrator/arquivos/p4_tabela_potenciacao.txt").readlines()    

    #cria listas e dicionários
    tabela_potenciacao_numeros = OrderedDict()
    tabela_histograma = OrderedDict()
    clusters = OrderedDict()
    clusters_full = OrderedDict()
    cluster = []
    clusters_selecionados = OrderedDict()
    vertices_selecionados = OrderedDict()
    
    #cria tabela com indice potenciação
    for linha in tabela_potenciacao:
        tabela_potenciacao_numeros[linha.split(' ')[0]] = float(linha.split(' ')[2].rstrip('\n'))     
        
    #separa dados para o histograma
    potenciacao_valores = []
    for item in tabela_potenciacao_numeros.values():
        potenciacao_valores.append(item)
    
    #gera histograma  
    maximo = parametros.faixa_histo + 3  
    intervalos = np.arange(0,maximo, parametros.faixa_histo)  

    n, bins, patches = plt.hist(potenciacao_valores, intervalos, facecolor='blue', alpha=0.5)
    pylab.savefig('extrator/arquivos/p5_grafo_histograma.png')     
    
    #inicializa json
    arq_json.write("[\n    {\n        \"name\": \"Histograma Clusters\",\n        \"other\": " + str(parametros.faixa_histo) + ",\n        \"data\":[\n")
    
    for idx,item in enumerate(n):
        arq_json.write("            {\n                \"bin\": " + str(bins[idx]) + ",\n                \"count\": " + str(int(item)) + "\n            }")
        if idx == (len(n) -1):
            arq_json.write("\n        ]\n    }\n]")         
        else:
            arq_json.write(",\n")      
        tabela_histograma[bins[idx + 1]] = item
        arq_tabela_histo.write(str(idx) + ' ' + str(bins[idx]) + '->'+  str(bins[idx + 1]) + ' ' + str(item) + '\n')
        
    arq_tabela_histo.close()    
    
    dados_histo = codecs.open("extrator/arquivos/p5_tabela_histograma.txt").readlines()
    lista_clusters = []
    for linha in dados_histo:
        if float(linha.split(' ')[2]) != 0.0: 
            lista_clusters.append(int(linha.split(' ')[0]))

    cont = 1
    for k, g in groupby(enumerate(reversed(lista_clusters)), lambda (i, x): i-x):
        clusters[cont] =  map(itemgetter(1), g)
        cont = cont + 1    
    

    cont = 1
    for item in clusters.values():
        limite_inferior = float(dados_histo[item[0]].split(' ')[1].split('->')[0])
        limite_superior = float(dados_histo[item[-1]].split(' ')[1].split('->')[1])
        arq_clusters.write('cluster ' + str(cont) + ' ' + str(limite_inferior) + ' ' + str(limite_superior) +'\n' )
        for linha in tabela_potenciacao:
            tema_num = linha.split(' ')[0]
            tema_nome = linha.split(' ')[1]
            tema_indice_potenciacao = float(linha.split(' ')[2].rstrip('\n'))   
            if (tema_indice_potenciacao >= limite_inferior) and (tema_indice_potenciacao <= limite_superior):
                # como aegs
                arq_clusters.write(str(tema_num).decode('utf-8') + ' ' + str(tema_nome).decode('utf-8') + ' ' + str(tema_indice_potenciacao) + '\n')
                cluster.append(str(tema_num).decode('utf-8') + ' ' + str(tema_nome).decode('utf-8') + ' ' + str(tema_indice_potenciacao))
        arq_clusters.write('\n')
        clusters_full[cont] = cluster
        cluster = []       
        cont = cont + 1    
    arq_clusters.close()
    
    #seleciona os clusters segundo criterio de corte
    for item in clusters_full.items():
        if len(item[1]) < ((parametros.f_corte)/100)*len(vertices_objs):
            clusters_selecionados[item[0]] = item[1]
        
    #cria lista de vertices selecionados do cluster
    for item in clusters_selecionados.items():
        for linha in item[1]:
            vertices_selecionados[linha.split(' ')[0]] = linha.split(' ')[1]      
    
    
    #armazena palavras para iniciar o teste de susbtantivo  
    TestaPalavra.objects.all().delete()
    aList = [TestaPalavra(palavra = nome, numero=int(numero), condicao='aguardando', resultado='null') for numero,nome in vertices_selecionados.items()]    
    TestaPalavra.objects.bulk_create(aList)

    #separa os substantivos
    #carrega lista de substantivos
    lista_substantivos = ListaDeSubstantivos.objects.all()
    lista_palavras = ListaDeSubstantivos.objects.all().values_list('palavra', flat=True)
    palavras = TestaPalavra.objects.filter(condicao__exact='aguardando')  

    # faz a primeira avaliação buscando os substantivos já classificados
    for palavra in palavras:
        if palavra.palavra in lista_palavras:
            a = lista_substantivos.get(palavra=palavra.palavra)
            palavra.condicao = 'finalizado'
            palavra.resultado = a.substantivo
            palavra.save()
            
    #carregas os temas ainda nao classificados
    palavras_faltantes = TestaPalavra.objects.filter(condicao__exact='aguardando').values_list('palavra',flat=True)   
    
    #manda as palavras para o usuário classificar    
    if palavras_faltantes:
        return render(request, 'extrator/extrator_resultados.html', {'testa_sub':'sim' , 'palavras_faltantes':palavras_faltantes})
    
   
    #cria vetor de vertices selecionados      
    temas_preselecionados = TestaPalavra.objects.filter(resultado='sim').values_list('numero','palavra')  
    temas_preselecionados = OrderedDict(temas_preselecionados)

    #inicializa relatório
    arq_relatorio.write('RELATÓRIO FINAL - TEMAS')
    arq_relatorio.write('\n\n\n')
    arq_relatorio.write('PARÂMETROS DE CLUSTERIZAÇÃO')
    arq_relatorio.write('\n\n')
    arq_relatorio.write('- Faixa de divisão do histograma: ' + str(parametros.faixa_histo) + '\n' ) 
    arq_relatorio.write('- Critério de exclusão do cluster: posssuir ' + str(parametros.f_corte) + '% dos nós totais ' + '(' + str((parametros.f_corte/100)*len(vertices_objs)) + ' de ' + str(len(vertices_objs)) + ')' + '\n\n'  ) 
    arq_relatorio.write('CLUSTERS SELECIONADOS')
    arq_relatorio.write('\n\n')
    for item in clusters_selecionados.items():
        arq_relatorio.write('Cluster ' + str(item[0]) + '\n')
        for linha in item[1]:
            arq_relatorio.write(str(linha.split(' ')[0]) + ' ' +  str(linha.split(' ')[1].encode('utf-8')) + ' ' + str(linha.split(' ')[2]) + '\n')
        arq_relatorio.write('\n')    
    arq_relatorio.write('TEMAS PRÉ-SELECIONADOS')
    arq_relatorio.write('\n\n') 
    for item in clusters_selecionados.items():               
        for linha in item[1]:
            arq_relatorio.write(str(linha.split(' ')[1].encode('utf-8')) + '\n')    
    arq_relatorio.write('\n\nSELEÇÃO FINAL DOS TEMAS\n\n')
    arq_relatorio.write('- Metodologia: Vizinho grau-1 \ frequência relativa dos bi-gramas\n')
    arq_relatorio.write('- Parâmetro: fb(frequência mínima de bigramas): ' + str(parametros.f_min_bigramas) + "% do total de bigramas\n")
    arq_relatorio.write('- Resultados: \n\n')
    arq_relatorio.write('Tema  ->  Vizinho  / Peso bigrama em relação ao vizinho / Frequência relativa \n\n')

    # calcula grau de entrada dos temas pre-selecionados      
    tabela_graus_entrada = OrderedDict()
    for tema in temas_preselecionados.values():       
        tema_entradas = tabela_bigramas.filter(vertice_f=tema)
        peso = 0      
        for bigrama in tema_entradas:            
            peso = peso + bigrama.peso            
        tabela_graus_entrada[tema] = peso   
    
    # verifica se o grau de entrada do vertice-destino é maior que 50% do peso do bigrama e cria lista de vertices a serem excluidos    
    temas_excluidos = [] 
    for tema_i in temas_preselecionados.values():
        for tema_f in temas_preselecionados.values():
            bigramas = tabela_bigramas.filter(vertice_i=tema_i,vertice_f=tema_f)            
            for bigrama in bigramas:  
                arq_relatorio.write(bigrama.vertice_i.encode('utf-8') + ' -> ' + bigrama.vertice_f.encode('utf-8') + ' - ' + str(bigrama.peso) + '/' + str(tabela_graus_entrada[tema_f]) + ' - ' +  str((bigrama.peso/tabela_graus_entrada[tema_f])*100) + '%\n')            
                if bigrama.peso >= (parametros.f_min_bigramas*tabela_graus_entrada[tema_f])/100:
                    temas_excluidos.append(tema_f)   
    
    
    #cria vetor de tema e IRT   
    temas_selecionados = OrderedDict()
    for tem in temas_preselecionados.values():
        vertice = TabelaRanking.objects.get(vertice_nome__exact=tem)
        temas_selecionados[tem] = ((float(vertice.potenciacao))/3)*100
       
    for tema in temas_excluidos:
        del temas_selecionados[tema]
    
    #escreve relatório e armazena temas no BD
    arq_relatorio.write('\n- Temas selecionados' + '(' + str(len(temas_selecionados)) + '):' '\n\n')
    for tema in temas_selecionados:
        arq_relatorio.write(tema.encode('utf-8') + '\n')

    #Salva temas no BD via bulk e inicializa protofrases    
    aList = [TemasNew(classificacao = 'subtema', tema = k, irt=v) for k,v in temas_selecionados.iteritems()]    
    TemasNew.objects.bulk_create(aList)
   
    arq_relatorio.write('\n\n- Temas excluídos' + '(' + str(len(temas_excluidos)) + '):' + '\n\n')
    for tema in temas_excluidos:
        arq_relatorio.write(tema.encode('utf-8') + '\n' )

    #fecha arquvos
    arq_relatorio.close()
    arq_json.close()

    #LÊ relatório    
    p4_relatorio = codecs.open("extrator/arquivos/p5_relatorio_temas.txt","r","utf-8").read()
  
    return render(request, 'extrator/extrator_resultados.html', {'documento_p4':p4_relatorio,'histo_p4':'h','goto':'passo4', 'muda_logo':'logo_sel_temas' })

def executa_passo_4(request):
    
    metricas_e_ranking(request)
    calcula_indice(request)
    selecionar_temas(request)

    #LÊ relatório    
    p4_relatorio = codecs.open("extrator/arquivos/p5_relatorio_temas.txt","r","utf-8").read()     
   
    
    return render(request, 'extrator/extrator_resultados.html', {'histo_p4':"hp4",'documento_p4':p4_relatorio,'goto': 'resultado-passo-4-histo'})    

######### FIM PASSO 4 ################################################################################################################################################################




########### PASSO 5 #############################################################################################################################################################################
 
def agrupar_temas(request):
    print "Selecionando os Subtemas..."

    #inicializa banco de dados   
    Clusters.objects.all().delete()  
    
    #cria arquivos
    arq_lista_agp = codecs.open("extrator/arquivos/p5_lista_adjacencias_agrupamento.txt", 'w', 'utf-8')
    
    #cria lista com os temas
    temas =[]
    temas_q = TemasNew.objects.all().values_list('tema', flat=True)
    string_grupo = ''
    for t in temas_q:
        temas.append(t)
        string_grupo = string_grupo + t + ' '    
    
    #cria pares de temas distintos
    pairs = list(itertools.combinations(temas, 2))   
    
    #carrega sentencas
    sentencas = codecs.open("extrator/arquivos/p3_texto_sentencas.txt","r",'utf-8').readlines()
    cluster = codecs.open("extrator/arquivos/p5_clusters.txt","r",'utf-8').readlines()      
    
    #inicializa variaves de teste
    temas_separados = {}

    #inicializa grupos
    a = Clusters(fim_de_arvore='nao',etapa =0, ident='0', caminho='0', q_subtemas=len(temas), nucleos='a definir', subtemas=string_grupo, situacao='processando')
    a.save()
    etapa = 1
    ident = 1
    caminho = '0'

    #carrega grupos a serem testados
    grupos = Clusters.objects.filter(situacao='processando')
    
    while grupos: 
        for grupo in grupos:
            
            ######## GERA REDE #######################################################################
            #separa os temas do grupo
            temas = grupo.subtemas.rstrip().split(' ')            
                
            #inicializa rede
            rede = nx.Graph()

            #gera os nos da rede
            for tema in temas:
                rede.add_node(tema)
            
            #cria pares de temas distintos
            pairs = list(itertools.combinations(temas, 2))
        
            #cria lista de adjacencias
            for par in pairs:
                cont = 0
                for sentenca in sentencas:        
                    lista_sent = sentenca.rstrip( ).split(' ')
                    if par[0] in lista_sent and par[1] in lista_sent:
                        cont = cont + 1
                arq_lista_agp.write(par[0] + ' ' + par[1] + ' ' + str(cont) + '\n')
                peso = float(cont)
                if cont > 0:
                    rede.add_edge(par[0], par[1], weight=peso)    
            ###########################################################################################
            
            ##### separa comunidade ###################################################################
            partition = community.best_partition(rede,weight='weight')
            ###########################################################################################
            
            #verifica em quantos grupos foi particionado
            quantidade_grupos = set(partition.values())
                    
            #se nao dividiu, termina
            if len(quantidade_grupos) == 1:
                grupo.situacao = 'finalizado'
                grupo.fim_de_arvore = 'sim'
                grupo.save()               
            
            #se nao, verifica se separou os nucleos   
            else:
                grupo.situacao = 'finalizado'
                grupo.save()
                #armazena nos grupos no BD
                for numero in quantidade_grupos:
                    novos_subtemas =[]
                    string_novos_subtemas = ''
                    caminho_novo = grupo.caminho + ' ' +str(ident)     
                    #cria novo conjunto de temas
                    for k,v in partition.iteritems():
                        if v == numero:
                            novos_subtemas.append(k)
                            string_novos_subtemas = string_novos_subtemas + k + ' '                  

                    a = Clusters(fim_de_arvore = 'nao', ident = ident, caminho = caminho_novo, etapa=etapa, q_subtemas=len(novos_subtemas), nucleos='a definir', subtemas=string_novos_subtemas, situacao='processando')        
                    a.save()
                    ident = ident + 1             
      
        grupos = Clusters.objects.filter(situacao='processando')     
        etapa = etapa + 1

    arq_lista_agp.close()       

    return render(request, 'extrator/extrator_resultados.html', {'goto':'passo5', 'muda_logo':'logo_agp_temas' })

def gerarMapaEResultados(request):
    print "Gerando resultados..."        
    #realtório
    arq_temas_subtemas = codecs.open("extrator/arquivos/p5_relatorio_temas_subtemas.txt", 'w', 'utf-8')
    arq_json = codecs.open(djangoSettings.STATIC_ROOT + "\\agora\\json\\p5_json_temas_subtemas.json", 'w', 'utf-8') 

    
    #inicializa o BD
    MapasTemasESubtemas.objects.all().delete()
    
    #carrega sentencas
    sentencas = codecs.open("extrator/arquivos/p3_texto_sentencas.txt","r",'utf-8').readlines()
    
    #carrega grupos
    grupos = Clusters.objects.filter(situacao='finalizado').filter(fim_de_arvore='sim')

    for grupo in grupos:
    
        #gera rede
        rede = nx.DiGraph()
        
        #inicializa nós
        temas = grupo.subtemas.rstrip().split(' ')
        
        #gera os nos da rede
        for tema in temas:
            rede.add_node(tema)

        #cria pares de temas distintos
        pairs = list(itertools.combinations(temas, 2))

        #cria lista de adjacencias
        for par in pairs:
            cont = 0
            for sentenca in sentencas:        
                lista_sent = sentenca.rstrip( ).split(' ')
                if par[0] in lista_sent and par[1] in lista_sent:
                    cont = cont + 1            
            peso = float(cont)
            if cont > 0:
                rede.add_edge(par[0], par[1], weight=peso)

        #cria tabelas
        tabela_graus = {}
       
        #gera metricas de centralidade       
        tabela_graus_t = nx.degree(rede, weight='weight')     
        tabela_graus = dict(tabela_graus_t)
        
        tema_maior_grau = max(tabela_graus.iteritems(), key=operator.itemgetter(1))[1]
        tema_selecionado = max(tabela_graus.iteritems(), key=operator.itemgetter(1))[0]
                      
        #salvar dados e calucal indices
        grupo.nucleos = tema_selecionado
        grupo.save()

        o = TemasNew.objects.get(tema__exact=tema_selecionado)
        o.classificacao = 'tema'
        o.save()      

        for k, v in tabela_graus.iteritems():
            obj = TabelaRanking.objects.get(vertice_nome__exact=k)
            potenciacao = obj.potenciacao
            if tema_maior_grau != 0:
                grau = float(v) / float(tema_maior_grau)
            else:
                grau = 0

            b = MapasTemasESubtemas(fim_de_arvore = grupo.fim_de_arvore, ident = grupo.ident, tema=tema_selecionado, subtema=k, grau=grau ,irt_l = potenciacao*grau)
            b.save()
      
    #escreve relatório    
    arq_temas_subtemas.write("RELATORIO FINAL DE TEMAS E SUBTEMAS \n\n\n")    
    temas = TemasNew.objects.filter(classificacao='tema').order_by('-irt') 
    
    for tema in temas:     
        arq_temas_subtemas.write('TEMA: ' + tema.tema + ' (' + str(tema.irt) + ') ' + '\n\n')
        objs = MapasTemasESubtemas.objects.filter(tema__exact=tema.tema).filter(fim_de_arvore='sim').order_by('-irt_l')
        for obj in objs:
            if obj.subtema != tema.tema:          
                arq_temas_subtemas.write(obj.subtema + ' (' + str(obj.irt_l) + ') '+ '\n')  
        arq_temas_subtemas.write('\n')
    
    arq_temas_subtemas.close()

    #cabeçalho
    arq_json.write("[\n{\n\"name\": \"Temas\",\n")
    arq_json.write("\"value\": " + str(2500) + ",\n")
    arq_json.write("\"size\": " + str(20) + ",\n")
    arq_json.write("\"parent\": \"null\" ,\n")
    arq_json.write("\"children\": [\n")
    arq_json.write("    {\n")

    
    for j, tema in enumerate(temas):    
        objs = MapasTemasESubtemas.objects.filter(tema__exact=tema.tema).filter(fim_de_arvore__exact = 'sim').exclude(subtema__exact=tema.tema).order_by('-irt_l')        
        obj_irt = TabelaRanking.objects.get(vertice_nome__exact=tema.tema)
        pot = obj_irt.potenciacao
        arq_json.write("        \"name\": \"" + tema.tema + "\",\n")
        arq_json.write("        \"value\": " + str(pot) + ",\n")
        arq_json.write("        \"size\": " + str(tema.irt/5) + ",\n")
        arq_json.write("        \"parent\": \"Temas\",\n")
        arq_json.write("        \"children\": [\n")        
     
        if objs:
            m = objs[0]            
        else:
            tam = 0
             
        for i, obj in enumerate(objs):
            tam = obj.irt_l / m.irt_l          
            if obj.subtema != tema.tema:                        
                arq_json.write("            {\n")
                arq_json.write("             \"name\": \"" + obj.subtema + "\",\n")    
                arq_json.write("             \"value\": " + str(obj.irt_l) + ",\n")    
                arq_json.write("             \"size\": " + str(tam*10) + ",\n")
                arq_json.write("             \"parent\": \"" + tema.tema + "\"\n")              
                arq_json.write("            }")
            if i == (len(objs) - 1):
                arq_json.write("\n")         
            else:                
                arq_json.write(",\n")
        
         #fecha tema
        if j == (len(temas) -1):
            arq_json.write("        ]\n    }\n")         
        else:
            arq_json.write("        ]\n    },\n    {\n")
       
    arq_json.write("    ]\n}\n]")
    arq_json.close()    

    #LÊ relatório    
    p5_relatorio = codecs.open("extrator/arquivos/p5_relatorio_temas_subtemas.txt","r","utf-8").read() 
          
    return render(request, 'extrator/extrator_resultados.html', {'p5_relatorio':p5_relatorio,'resultados_p5':'res','goto':'passo5', 'muda_logo':'logo_gmr_temas' })

def executa_passo_5(request):
            
    gerarMapaEResultados(request)
    agrupar_temas(request)

    #LÊ relatório    
    p5_relatorio = codecs.open("extrator/arquivos/p5_relatorio_temas_subtemas.txt","r","utf-8").read()   
    
    return render(request, 'extrator/extrator_resultados.html', {'p5_relatorio':p5_relatorio,'resultados_p5':'res','goto':'passo5', 'muda_logo':'logo_gmr_temas' })


######### FIM PASSO 5 ################################################################################################################################################################




########### PASSO 6 #############################################################################################################################################################################

def processarProtofrases(request):
    print "Avaliando as protofrases..."
    parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
    #Nesta etapa, todas as protofrases recebem um peso formado pela soma dos pesos das arestas e um cirtério de corte
   
    #inicializa dados da extrcao
    SentencasAvaliadas.objects.all().delete()

    #carrega arquivos 
    sentencas = codecs.open("extrator/arquivos/p3_texto_sentencas.txt","r",'utf-8').readlines()
    lista_de_adjacencias = codecs.open("extrator/arquivos/p3_lista_adjacencias.txt","r",'utf-8').readlines()
    arq_texto_preprocessado_vet = codecs.open("extrator/arquivos/p2_texto_preprocessado_vetorizado.txt","r",'utf-8').readlines()
    arq_sentencas = codecs.open("extrator/arquivos/p3_texto_sentencas.txt", "r", 'utf-8').readlines()
    
    #carrega os grupos
    grupos = Clusters.objects.filter(fim_de_arvore='sim')
   
    #inicializa listas
    sentencas_avaliadas = []
    sentencas_mapeadas = OrderedDict()

    ### mapeia as sentencas: busca a protofrase e sua frase original e armazena ambas em um dicionário ###############################################################################################
    sentencas_pp_vet = []
    senten = ''
   
    for linha in arq_texto_preprocessado_vet:
        if linha.rstrip() != '.':
            senten = senten + linha.rstrip() + ' '
        
            
            #senten = senten + ' ' + str(linha.encode('utf-8')).rstrip()

        if linha.rstrip() == '.':
            senten = senten.rstrip()
            sentencas_pp_vet.append(senten)           
            senten = ''
            
    print 'Esse valor ' + str(len(arq_sentencas)) + ' deve ser igual a este ' + str(len(sentencas_pp_vet)) + ' . Caso seja diferente, verificar linha 1450'
    
    if len(arq_sentencas) != len(sentencas_pp_vet):
        return render(request, 'extrator/extrator_resultados.html', {'goto': 'passo5', 'muda_logo':'logo_protofrases','mess':'ERRO NA QUANTIDADE DE SENTENCAS' })
    
    for indx, linha in enumerate(arq_sentencas):
        sentencas_mapeadas[linha] = sentencas_pp_vet[indx]

    ##################################################################################################################################################################################
    
    string = []
    
    for grupo in grupos:
        lista_de_nos = []
        lista_de_nos_dist = []
        tabela_graus = []        
        #separa as palavras       
        vertices = grupo.subtemas.rstrip().split(' ')
       
        #Separa as sentencas que contém as palavras do grupo
        sentencas_grupo = []
        sentencas_original = []
        bag = []
        for idx, linha in enumerate(arq_sentencas):
            bag = linha.rstrip().split(' ')
            if not set(vertices).isdisjoint(bag):
                sentencas_grupo.append(linha.rstrip())
                sentencas_original.append(sentencas_pp_vet[idx])
       
        #cria lista de adjancecias
        lista_adjacencias = OrderedDict()
        for sentenca in sentencas_grupo:             
            bigrama = 'ok'
            palavras_sentenca = sentenca.rstrip().split(' ')
            for i, palavra in enumerate(palavras_sentenca):
                lista_de_nos.append(palavra)
                try:                                             
                    bigrama = palavras_sentenca[i] + ' ' + palavras_sentenca[i + 1]                    
                except:
                    bigrama = 'fim' 
                if bigrama != 'fim':
                    try:   
                        lista_adjacencias[bigrama] = lista_adjacencias[bigrama] + 1
                    except:
                        lista_adjacencias[bigrama] = 1            

        #gera rede e tabelade graus
        rede = nx.DiGraph()
        lista_de_nos_dist = list(set(lista_de_nos))
        
        for item in lista_de_nos_dist:
            rede.add_node(item)
        
        for k, v in lista_adjacencias.iteritems():
            nodes = k.split(' ')
            rede.add_edge(nodes[0], nodes[1], weight=int(v))
        
        tabela_graus = nx.degree(rede, weight='weight')
        
        # faz aguma coisa 
        for idx, sentenca in enumerate(sentencas_grupo):
            peso = 0            
            palavras_sentenca = sentenca.split(' ')
            maior_grau = 0
            corte = 0
            bigrama = 'ok'
            string_graus_l = []
            
            #acha o maior grau:
            for i, palavra in enumerate(palavras_sentenca):                
                try:                                           
                    bigrama = palavras_sentenca[i] + ' ' + palavras_sentenca[i+1]                      
                except:
                    bigrama = 'fim'
                if bigrama != 'fim':
                    for k,v in lista_adjacencias.iteritems():
                        if bigrama in k and float(v) > maior_grau:
                            maior_grau = float(v)                 
            
            grau_corte = (float(parametros.corte_n/100))*maior_grau
            if grau_corte < 1:
                grau_corte = 1.0             
            
            for i, palavra in enumerate(palavras_sentenca):
                bigrama = 'ok'
                try:                                            
                    bigrama = palavras_sentenca[i] + ' ' + palavras_sentenca[i+1]
                except:
                    bigrama = 'fim'
                if bigrama != 'fim':
                    for k,v in lista_adjacencias.iteritems():
                        if bigrama == k:                              
                            if float(v) > grau_corte:
                                string_graus_l.append(str(v))         
                                peso = peso + float(v)
                            else:
                                string_graus_l.append(str(0))         
                                corte = corte + 1
            if not string_graus_l:
                string_graus_l.append(str(0))
            string_graus = ' '.join(string_graus_l)                              
            string.append([ grupo.nucleos, sentenca, sentencas_original[idx], str(peso), str(corte), string_graus ])
    
    #salva dados no BD
    aList = [SentencasAvaliadas(tema=sent[0], subtema='a definir', proto=sent[1] , frase=sent[2] , peso=sent[3] , corte=sent[4], irse=0, string_graus=sent[5]) for sent in string]    
    SentencasAvaliadas.objects.bulk_create(aList) 

    return render(request, 'extrator/extrator_resultados.html', {'goto': 'passo5', 'muda_logo':'logo_protofrases' })


def mapearEextrair(request):
    print "Extraindo as frases..."
    #Separa as setencças por cluster e subtema
    
    #carrega sentanças já avaliadas
    SentencasExtraidas.objects.all().delete()

    #carregas os temas
    temas_subtemas = Clusters.objects.filter(fim_de_arvore='sim')

    #inicializa listas
    sentencas_mapeadas = []
    bag_protos =[]
    ident = 0
    for itemm in temas_subtemas:        
        palavras = itemm.subtemas.rstrip().split(' ')
        for palavra in palavras:             
            sentencas = SentencasAvaliadas.objects.filter(tema__exact=itemm.nucleos).filter(proto__icontains=palavra).order_by('peso').order_by('-corte')
            obj_maior_peso = max(sentencas, key=attrgetter('peso'))
            maior_peso = obj_maior_peso.peso           
            for sent in sentencas:            
                if (itemm.nucleos != palavra):
                    if sent.proto not in bag_protos:
                        if maior_peso == 0:
                            irse = 0
                        else:
                            irse = int((sent.peso / maior_peso)*100)
                        if irse > 80:
                            representatividade = 'altissima'
                        if irse > 60 and irse <= 80:
                            representatividade = 'alta'
                        if irse > 40 and irse <= 60:                                    
                            representatividade = 'media'
                        if irse > 20 and irse <= 40:
                            representatividade = 'baixa'
                        if irse >= 0 and irse <= 20:
                            representatividade = 'baixissima'                       
                        ident = ident + 1
                        sentencas_mapeadas.append([itemm.nucleos, palavra, sent.frase, sent.peso, sent.corte, irse, representatividade, sent.proto, sent.string_graus, ident])
                        
                        bag_protos.append(sent.proto)
            bag_protos = []  
    
    #salva dados no BD
    aList = [SentencasExtraidas(ident=sent[9], tema=sent[0], subtema=sent[1], frase=sent[2] , proto=sent[7], string_graus=sent[8], peso=sent[3] , corte=sent[4], irse=sent[5], representatividade=sent[6]) for sent in sentencas_mapeadas]    
    SentencasExtraidas.objects.bulk_create(aList)

    return render(request, 'extrator/extrator_resultados.html', {'goto':'passo5', 'muda_logo':'logo_map_extracao'})

def extrairNucleos(request):
    print 'Extraindo nucleos...'
    
    #inicilaiza coisas do BD
    parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
    SentencasNucleos.objects.all().delete()
    
    arq_entrada_lematizador = codecs.open("extrator/arquivos/p6_entrada_lematizador.txt","w",'utf-8')
    
    #Carrega Objetos
    objetos = SentencasExtraidas.objects.all()

    #cria entrada do lematizador
    for obj in objetos:
        arq_entrada_lematizador.write(str(obj.ident) + ' ' + obj.frase.rstrip() + '.\n')
        
    arq_entrada_lematizador.close()   
    
    #Abre o Bash e executa o lematizador no texto inicial
    is32bit = (platform.architecture()[0] == '32bit')
    system32 = os.path.join(os.environ['SystemRoot'],
                        'SysNative' if is32bit else 'System32')
    bash = os.path.join(system32, 'bash.exe')   
    p = subprocess.check_call('"%s" -c "cd Linguakit-master ; ./linguakit lem pt ../extrator/arquivos/p6_entrada_lematizador.txt > ../extrator/arquivos/p6_saida_lematizador.txt ; unix2dos ../extrator/arquivos/p2_saida_lematizador.txt"' % bash, shell=True)
    
    #processa saida do lematizador e gera arquivo com sequencias lematizadas
    saida_lematizador = codecs.open("extrator/arquivos/p6_saida_lematizador.txt","r","utf-8")  
    arq_sentencas_lematizadas = codecs.open("extrator/arquivos/p6_sentencas_lematizadas.txt", "w", 'utf-8')
    arq_sentencas_org_lematizadas = codecs.open("extrator/arquivos/p6_sentencas_originais_lem.txt","w",'utf-8')    
  
    string = ''
    string_org = ''
    lista_strings_org =[]
    lista_strings = []
    cont = 0
    for linha in saida_lematizador:            
        if linha != "\n":
            try:           
                linha.rstrip().split(' ')[2]
                if linha[0] != ' ':    
                    word_lem = linha.rstrip().split(' ')[1]
                    word_org = linha.rstrip().split(' ')[0]
                    if word_lem == '.':
                        arq_sentencas_lematizadas.write('.\n')
                        arq_sentencas_org_lematizadas.write('.\n')

                        lista_strings.append(string.rstrip())
                        lista_strings_org.append(string_org.rstrip())

                        string = ''
                        string_org = ''
                     
                    else:
                        arq_sentencas_lematizadas.write(word_lem.rstrip() + ' ')
                        arq_sentencas_org_lematizadas.write(word_org.rstrip() + ' ')
                        
                        string = string + word_lem.rstrip() + ' '
                        string_org = string_org.rstrip() + word_org.rstrip() + ' '

            except:
                if linha[0] != ' ':    
                    word_lem = linha.rstrip().split(' ')[0]                
                    if word_lem == '.':
                        arq_sentencas_lematizadas.write('.\n')
                        arq_sentencas_org_lematizadas.write('.\n')
                        
                        lista_strings.append(string.rstrip())
                        lista_strings_org.append(string_org.rstrip())
                        
                        string = ''
                        string_org = ''                      
                    else:
                        arq_sentencas_lematizadas.write(word_lem.rstrip() + ' ')
                        arq_sentencas_org_lematizadas.write(word_lem.rstrip() + ' ')
                        
                        string = string + word_lem.rstrip() + ' '
                        string_org = string_org.rstrip() + word_lem.rstrip() + ' '
                     
    arq_sentencas_lematizadas.close()
    arq_sentencas_org_lematizadas.close()
    
    sentencas_nucleos = []
    for obj in objetos:
       
        #lista_adjacencias_orig = OrderedDict()
        lista_adjacencias_orig = []
        palavras_proto_l =  obj.proto.rstrip().split(' ')
        if len(palavras_proto_l) > 1:
            
            # GERA LISTA DE ADJACENCIAS
            #lista_de_adjacencias = OrderedDict()
            lista_de_adjacencias = []
            graus_l = obj.string_graus.rstrip().split(' ')             
            if len(palavras_proto_l) != 1:           
                for idx, palavra in enumerate(palavras_proto_l):                 
                    fim = 'nao'
                    bigrama = ''
                    try:
                        bigrama = palavras_proto_l[idx] + ' ' + palavras_proto_l[idx + 1]
                    except:
                        fim = 'fim'
                    if fim == 'nao':               
                        lista_de_adjacencias.append([bigrama, graus_l[idx]])
                        #lista_de_adjacencias[bigrama] = graus_l[idx]
            else:
                lista_de_adjacencias.append([palavras_proto[0],graus_l[0]])
                #lista_de_adjacencias[palavras_proto_l[0]] = graus_l[0]        
            
            # pega frase lematizada relativa à protofrase        
            sentenca_l = OrderedDict()
            for sent in lista_strings:
                pals = sent.rstrip().split(' ')
                if int(pals[0]) == obj.ident:               
                    sentenca = sent
            
            
            #Cria dicionario com as palavras de cada sentenca original
            sentenca_l_l = sentenca.rstrip().split(' ')        
            count = 0
            for item in sentenca_l_l:
                sentenca_l[count] = item
                count = count + 1

            #Cria lista de adjacencias com as palavras intermediarias: (A x y c Z -> 3...)
            bigramas =[]
            for r in lista_de_adjacencias:
                bigramas.append(r[0])            
            #bigramas = lista_de_adjacencias.keys()
        
            for linha in bigramas:
                palavras_bigrama = linha.split(' ')            
                flag1 = 'no1'
                flag2 = 'no2'                
                string = ''
                elim =[]
                for ind, palavra in sentenca_l.iteritems():                                     
                    if flag1 == 'ok' and flag2 == 'no2':
                        string = string + palavra + ' '                     
                    
                    if palavra == palavras_bigrama[0] and flag1 == 'no1':
                        string = string + palavra + ' ' 
                        flag1 = 'ok'
                        
                    else:
                        if palavra == palavras_bigrama[1] and flag1 == 'ok':
                            flag2 = 'ok'                                 
                            for h in lista_de_adjacencias:
                                if linha == h[0]:
                                    valor = h[1]                            
                            #ista_adjacencias_orig[string] = lista_de_adjacencias[linha]                    
                            #lista_adjacencias_orig[string] = valor
                            lista_adjacencias_orig.append([string,valor])
                            for j in elim:
                                del sentenca_l[j]  
                            break                               
                    
                    elim.append(int(ind))         
           
            #Extrai os trechos com peso maior que 0 
            primeiro = 'sim'
            string = ''
            lista_extracao_l = []
            cont = 0
            tam = len(lista_adjacencias_orig)
            for linha_adj in lista_adjacencias_orig:                
                #print k
                if linha_adj[1] == str(0):                    
                    if string:
                        lista_extracao_l.append(string.rstrip())
                    string = ''
                    primeiro = 'sim'
                else:
                    if primeiro == 'sim':
                        string = string + linha_adj[0].rstrip() + ' '
                        primeiro = 'nao'
                        if (cont + 1) == tam :
                            lista_extracao_l.append(string.rstrip())
                    else:
                        pls = linha_adj[0].rstrip().split(' ')
                        del pls[0]
                        nova_string = ' '.join(pls)
                        string = string + nova_string.rstrip() + ' '
                        if (cont + 1) == tam :
                            lista_extracao_l.append(string.rstrip())
            
                cont = cont + 1
       
            #mapear os dados extraidos das frases originais
            lista_extracao_o =[]
            
            arq_l = codecs.open("extrator/arquivos/p6_sentencas_lematizadas.txt","r","utf-8")
            arq_o = codecs.open("extrator/arquivos/p6_sentencas_originais_lem.txt","r","utf-8") 
            
            set_lematizadas = arq_l.readlines()
            set_originais = arq_o.readlines()

            set_l_dict = OrderedDict()
            set_o_dict = OrderedDict()           
            
            for item in set_lematizadas:                
                num = item.rstrip().split(' ')[0]
                if int(num) == obj.ident:
                    set_l = item.rstrip().split(' ')
                    cont = 0
                    for i in set_l:
                        set_l_dict[cont] = i
                        cont = cont + 1
           
            for item in set_originais:
                num = item.rstrip().split(' ')[0]
                if int(num) == obj.ident:                  
                    set_o = item.rstrip().split(' ')
                    cont = 0
                    for i in set_o:
                        set_o_dict[cont] = i
                        cont = cont + 1
            
            #CONTINUAR A PARTIR DAQUI: TENHO A SENTENCA LEMATIZA INDEXADA, SENTENCA ORIGINAL INDEXADA E A EXTRACAO LEMATIZADA. PRECISO ACHAR O LUGAR EXATO NA SENTENCA LEMATIZADA E PEGAR OS INDICES E COM OS INDICES ACHAR NA SENTENA ORIGINAL
            f_o_extraidas = []
            f_o_extraida_string = ''
            
            for j in lista_extracao_l:
                palavras_set_extraida = j.rstrip().split(' ')
                primeira_palavra = palavras_set_extraida[0]

                #procura primeira palavra na sentenca lematizada
                pp_set_ext_indice = []
                for k, v in set_l_dict.iteritems():
                    if primeira_palavra == v:
                        pp_set_ext_indice.append(k)

                #caso haja apenas uma palavra, já mapeia e extrai a fase original
                frase_orig_extraida = ''
                if len(pp_set_ext_indice) == 1:
                    tamanho = len(palavras_set_extraida)
                    inicio = int(pp_set_ext_indice[0])
                    fim = inicio + tamanho                     
                    for g in range(inicio, fim):
                        frase_orig_extraida = frase_orig_extraida + set_o_dict[g] + ' '
                    f_o_extraidas.append(frase_orig_extraida)
                
                else:
                    for item in pp_set_ext_indice:                        
                        tamanho = len(palavras_set_extraida)
                        inicio = item
                        fim = inicio + tamanho
                        teste = []
                        idt = 0
                        for u in range(inicio, fim):                           
                            if set_l_dict[u] == palavras_set_extraida[idt]:
                                teste.append('ok')
                            else:
                                teste.append('dif')
                            idt = idt + 1
                        if not 'dif' in teste:
                            for g in range(inicio, fim):
                                frase_orig_extraida = frase_orig_extraida + set_o_dict[g] + ' '
                            f_o_extraidas.append(frase_orig_extraida)
                            break
                f_o_extraida_string = '  */*  '.join(f_o_extraidas)

            f_o_extraida_string_corrigida = unsplit(f_o_extraida_string)        
            sentencas_nucleos.append([obj.ident, obj.tema, obj.subtema, obj.proto, obj.frase, f_o_extraida_string_corrigida, obj.string_graus, obj.peso, obj.representatividade, obj.irse])

        else:
            sentencas_nucleos.append([obj.ident, obj.tema, obj.subtema, obj.proto, obj.frase, obj.frase, obj.string_graus, obj.peso, obj.representatividade, obj.irse])

    #salva dados no BD
    aList = [SentencasNucleos(ident=sent[0], tema=sent[1], subtema=sent[2], frase=sent[4] , proto=sent[3], nucleo=sent[5].rstrip(), string_graus=sent[6], peso=sent[7] , representatividade=sent[8], irse=sent[9]) for sent in sentencas_nucleos]    
    SentencasNucleos.objects.bulk_create(aList)
    
    return render(request, 'extrator/extrator_resultados.html', {'goto':'passo6', 'muda_logo':'logo_enucleos'})    

def extraiSentencasGlobais(request):
    
    #prepara BD
    SentencasGlobais.objects.all().delete()

    #Inicializa arquivo TSV
    arq_tsv = codecs.open(djangoSettings.STATIC_ROOT + "\\agora\\json\\p6_json_data_globais.tsv", 'w', 'utf-8') 
    
    #carega parametros
    parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
    par = parametros.radio_r
    list_par = [int(x) for x in par.split(" ")]
    
    #carrega dados e inicializa listas
    objetos = SentencasNucleos.objects.all()
    objetos_distintos = SentencasNucleos.objects.values_list('nucleo', flat=True).distinct()
    resultados = OrderedDict()
    resultados_rankeados = OrderedDict()
    resultados_rankeados_norm = []
    representatividade = ''
    
    for obj_d in objetos_distintos:
        peso = 0
        for obj in objetos:
            if obj_d == obj.nucleo:
                peso = peso + obj.peso
        resultados[obj_d] = peso
    
    resultados_rankeados = sorted(resultados.iteritems(), key=operator.itemgetter(1))
    
    maior_peso = max(resultados.iteritems(), key=operator.itemgetter(1))[1]

    for item in resultados_rankeados:
        
        peso_f = int(float(item[1])/float(maior_peso)*100)        
         
        if peso_f > 80:
            representatividade = 'altissima'
        if peso_f > 60 and peso_f <= 80:
            representatividade = 'alta'
        if peso_f > 40 and peso_f <= 60:                                    
            representatividade = 'media'
        if peso_f > 20 and peso_f <= 40:
            representatividade = 'baixa'
        if peso_f >= 0 and peso_f <= 20:
            representatividade = 'baixissima'  

        resultados_rankeados_norm.append([item[0], item[1], peso_f, representatividade])
    
    #salva dados no BD
    aList = [SentencasGlobais(nucleo=sent[0], peso=sent[1], irseg=sent[2], representatividade=sent[3] ) for sent in resultados_rankeados_norm]    
    SentencasGlobais.objects.bulk_create(aList)

    #carrega objetos a serem exibidos    
    lll = []
    for num in list_par:
        if num == 5:
            lll.append('altissima')
        if num == 4:
            lll.append('alta')        
        if num == 3:
            lll.append('media')        
        if num == 2:
            lll.append('baixa')        
        if num == 1:
            lll.append('baixissima')         
    
    lpk =[]
    obj_children_pk = SentencasGlobais.objects.all()
    for obn in obj_children_pk:
        if obn.representatividade in lll:
            lpk.append(obn.pk)
    
    objetos = SentencasGlobais.objects.filter(pk__in=lpk).exclude(irseg__exact=0).order_by('-irseg')

    arq_tsv.write("Nucleo\tIrseg\tIdent\tRepresentatividade\n")
    cont = 0
    for obj in objetos:
        ident = 'ident_' + str(cont)
        arq_tsv.write(obj.nucleo + '\t' + str(float(obj.irseg)/100) + '\t' + ident + '\t' + obj.representatividade + '\n')          
        cont = cont + 1
    
    return render(request, 'extrator/extrator_resultados.html', {'goto':'p6-result', 'muda_logo':'logo_eglobais','resultados_p7':'resultados_p7',})    


def calcula_indice_representatividade(request):
    print "Calculando representatividade e montando resultados finais..."

    
    #iniccializacoes
    temas = TemasNew.objects.filter(classificacao='tema').order_by('-irt') 
    arq_json = codecs.open(djangoSettings.STATIC_ROOT + "\\agora\\json\\p6_json_sentencas_extraidas.json", 'w', 'utf-8')
    arq_relatorio = codecs.open("extrator/arquivos/p6_relatorio_final_extracao.txt", 'w', 'utf-8')

    parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
    par = parametros.radio_r
    list_par = [int(x) for x in par.split(" ")]
        
    #Inicializa relatório
    arq_relatorio.write("RELATORIO FINAL DE EXTRACAO\n\n\n")    
    
    #cabeçalho
    arq_json.write("[\n{\n\"name\": \"Temas\",\n")
    arq_json.write("\"value\": " + str(2500) + ",\n")
    arq_json.write("\"size\": " + str(20) + ",\n")
    arq_json.write("\"parent\": \"#fff\" ,\n")
    arq_json.write("\"children\": [\n")
    arq_json.write("    {\n")
    
    for j, tema in enumerate(temas):
        arq_relatorio.write('\nTEMA: ' + tema.tema + '\n\n')
        arq_relatorio.write('subtema / frase / irse / nucleo / representatividade \n')       
        objs = MapasTemasESubtemas.objects.filter(tema__exact=tema.tema).filter(fim_de_arvore__exact = 'sim').exclude(subtema__exact=tema.tema).order_by('-irt_l')
        obj_irt = TabelaRanking.objects.get(vertice_nome__exact=tema.tema)
        
        pot = obj_irt.potenciacao
        arq_json.write("        \"name\": \"" + tema.tema + "\",\n")
        arq_json.write("        \"value\": " + str(pot) + ",\n")
        arq_json.write("        \"size\": " + str(tema.irt / 5) + ",\n")
        arq_json.write("        \"place\": " + "\"meta\"" + ",\n")
        arq_json.write("        \"repr\": " + "\"#fff\"" + ",\n")
        arq_json.write("        \"repr2\": " + "\"steelblue\"" + ",\n")
        arq_json.write("        \"parent\": \"Temas\",\n")
        arq_json.write("        \"children\": [\n")       
        if objs:
            m = objs[0]            
        else:
            tam = 0
             
        for i, obj in enumerate(objs):
            tam = obj.irt_l / m.irt_l          
            if obj.subtema != tema.tema:
                                      
                arq_json.write("            {\n")
                arq_json.write("             \"name\": \"" + obj.subtema + "\",\n")    
                arq_json.write("             \"value\": " + str(obj.irt_l) + ",\n")    
                arq_json.write("             \"size\": " + str(tam * 10) + ",\n")
                arq_json.write("             \"place\": " + '\"meta\"' + ",\n")
                arq_json.write("             \"repr\": " + '\"#fff\"' + ",\n")
                arq_json.write("             \"repr2\": " + '\"steelblue\"' + ",\n")
                arq_json.write("             \"parent\": \"" + tema.tema + "\",\n")
                arq_json.write("             \"children\": [\n")
                
                lll = []
                for num in list_par:
                    if num == 5:
                        lll.append('altissima')
                    if num == 4:
                        lll.append('alta')        
                    if num == 3:
                        lll.append('media')        
                    if num == 2:
                        lll.append('baixa')        
                    if num == 1:
                        lll.append('baixissima')         
                
                lpk =[]
                obj_children_pk = SentencasNucleos.objects.filter(tema__exact=tema.tema).filter(subtema__exact=obj.subtema).order_by('-irse')
                for obn in obj_children_pk:
                    if obn.representatividade in lll:
                        lpk.append(obn.pk)                              
                
                obj_children = SentencasNucleos.objects.filter(pk__in=lpk).order_by('-irse')               
                if obj_children:
                    for p, obj_c in enumerate(obj_children):
                        obj_nucleo = SentencasNucleos.objects.filter(ident__exact=obj.ident)
                             
                        arq_relatorio.write(obj_c.subtema + '   /   ' + obj_c.frase + '   /   ' + obj_c.nucleo + '   /   ' + str(obj_c.irse) + '   /   ' + obj_c.representatividade + '\n')
                        
                        if obj_c.representatividade == 'altissima':
                            cor = '#FF0000'
                        if obj_c.representatividade == 'alta':
                            cor = '#B65B00'
                        if obj_c.representatividade == 'media':
                            cor = '#E67404'
                        if obj_c.representatividade == 'baixa':
                            cor = '#FEFE80'
                        if obj_c.representatividade == 'baixissima':
                            cor = '#6CE200'                     
                        arq_json.write("                {\n")
                        arq_json.write("                     \"name\": \"" + obj_c.nucleo.replace("\"", "") + "\",\n")    
                        arq_json.write("                     \"value\": " + str(obj.irt_l) + ",\n")    
                        arq_json.write("                     \"size\": " + str(5) + ",\n")
                        arq_json.write("                     \"place\": " + '\"end\"' + ",\n")
                        arq_json.write("                     \"repr\": \"" + cor + "\",\n")
                        arq_json.write("                     \"repr2\": \"" + cor + "\",\n")
                        arq_json.write("                     \"parent\": \"" + obj_c.subtema + "\"\n")
                        arq_json.write("                }")
                        
                        if p == (len(obj_children) - 1):
                            arq_json.write("\n                ]\n")         
                        else:                
                            arq_json.write(",\n")
                else:
                    arq_relatorio.write(obj.subtema + '   /   ' + "Nao foi possivel extrair frases\n")
                    arq_json.write("                {\n")
                    arq_json.write("                     \"name\": \"" + "nao foi possivel extrair frases" + "\",\n")    
                    arq_json.write("                     \"value\": " + "0" + ",\n")    
                    arq_json.write("                     \"size\": " + str(5) + ",\n")
                    arq_json.write("                     \"place\": " + '\"end\"' + ",\n")
                    arq_json.write("                     \"repr\": \"" + "black" + "\",\n")
                    arq_json.write("                     \"repr2\": \"" + "black" + "\",\n")
                    arq_json.write("                     \"parent\": \"" + obj_c.subtema + "\"\n")
                    arq_json.write("                }")
                    arq_json.write("\n                ]\n")  
                
                arq_relatorio.write('\n')           
            
            if i == (len(objs) - 1):
                arq_json.write("            }\n")         
            else:                
                arq_json.write("            },\n")
        
         #fecha tema
        if j == (len(temas) -1):
            arq_json.write("        ]\n    }\n")         
        else:
            arq_json.write("        ]\n    },\n    {\n")
       
    arq_json.write("    ]\n}\n]")
    arq_json.close()
    arq_relatorio.close()

    #LÊ relatório    
    p6_relatorio = codecs.open("extrator/arquivos/p6_relatorio_final_extracao.txt", "r", "utf-8").read()
        
    return render(request, 'extrator/extrator_resultados.html', {'relatorio_p6':p6_relatorio,'resultados_p6':'p6','goto':'p6-result', 'muda_logo':'logo_repres','fim':'fim'})
    
def executa_passo_6(request):  

    calcula_indice_representatividade(request)
    mapearEextrair(request)
    processarProtofrases(request)
    extrairNucleos(request)

    #LÊ relatório    
    p6_relatorio = codecs.open("extrator/arquivos/p6_relatorio_final_extracao.txt","r","utf-8").read()  
    
    return render(request, 'extrator/extrator_resultados.html', {'relatorio_p6':p6_relatorio,'resultados_p6':'res','goto':'p6-result', 'muda_logo':'logo_gmr_temas' })

######### FIM PASSO 6 ################################################################################################################################################################



############### FUNCOES DE AUXILIO ##########################################################################################################################################################
def unsplit(sentenca):  
        
    string = sentenca
    
    #do(s), da(s)
    string = re.sub(r'\bde o\b', u'do', string)
    string = re.sub(r'\bde a\b', u'da', string)
    string = re.sub(r'\bde os\b', u'dos', string)
    string = re.sub(r'\bde as\b', u'das', string)        

    #ao, à, aos, às
    string = re.sub(r'\ba o\b', u'ao', string)
    string = re.sub(r'\ba a\b', u'à', string)
    string = re.sub(r'\ba os\b', u'aos', string)
    string = re.sub(r'\ba as\b', u'às', string)
    
    #àquele(s), àquela(s). àquilo, aonde
    string = re.sub(r'\ba aquel\b', u'àquele', string)
    string = re.sub(r'\ba aqueles\b', u'àqueles', string)
    string = re.sub(r'\ba aquela\b', u'àquela', string)
    string = re.sub(r'\ba aquelas\b', u'àquelas', string)
    string = re.sub(r'\ba onde\b', u'aonde', string)
    
    #dele(s), dela(s)
    string = re.sub(r'\bde ele\b', u'dele', string)
    string = re.sub(r'\bde eles\b', u'deles', string)
    string = re.sub(r'\bde ela\b', u'dela', string)
    string = re.sub(r'\bde las\b', u'delas', string)
    
    # #deste(s), desta(s), desse(s), dessa(s), daquele(s), daquela(s), disto, disso, daquilo
    string = re.sub(r'\bde estes\b', u'destes', string)
    string = re.sub(r'\bde esta\b', u'desta', string)
    string = re.sub(r'\bde estas\b', u'destas', string)
    string = re.sub(r'\bde esse\b', u'desse', string)
    string = re.sub(r'\bde esses\b', u'desses', string)
    string = re.sub(r'\bde este\b', u'destes', string)
    string = re.sub(r'\bde essa\b', u'dessa', string)
    string = re.sub(r'\bde isso\b', u'disso', string)
    string = re.sub(r'\bde aquele\b', u'daquele', string)
    string = re.sub(r'\bde aquela\b', u'daquela', string)
    string = re.sub(r'\bde aqueles\b', u'daqueles', string)
    string = re.sub(r'\bde aquelas\b', u'daquelas', string)
    string = re.sub(r'\bde aquilo\b', u'daquilo', string)

    #daqui, daí, ali, acolá, donde, doutro(s), doutra(s)
    string = re.sub(r'\bde aqui\b', u'daqui', string)
    string = re.sub(r'\bde aí\b', u'daí', string)
    string = re.sub(r'\bde acolá\b', u'dacolá', string)        
    
    #no(s), na(s)
    string = re.sub(r'\bem o\b', u'no', string)
    string = re.sub(r'\bem os\b', u'nos', string)
    string = re.sub(r'\bem a\b', u'na', string)
    string = re.sub(r'\bem as\b', u'nas', string)

    #nele(s)
    string = re.sub(r'\bem ele\b', u'nele', string)
    string = re.sub(r'\bem eles\b', u'neles', string)       
    
    #neste(s), nesta(s), nesse(s), nessa(s), naquele(s), naquela(s), nisto, nisso, naquilo
    string = re.sub(r'\bem este\b', u'neste', string)
    string = re.sub(r'\bem estes\b', u'nestes', string)
    string = re.sub(r'\bem esta\b', u'nesta', string)
    string = re.sub(r'\bem estas\b', u'nestas', string)
    string = re.sub(r'\bem isto\b', u'nisto', string)
    string = re.sub(r'\bem esse\b', u'nesse', string)
    string = re.sub(r'\bem esses\b', u'nesses', string)
    string = re.sub(r'\bem essa\b', u'nessa', string)
    string = re.sub(r'\bem essas\b', u'nessas', string)
    string = re.sub(r'\bem isso\b', u'nisso', string)
    string = re.sub(r'\bem aquele\b', u'naquele', string)
    string = re.sub(r'\bem aquela\b', u'naquela', string)
    string = re.sub(r'\bem aqueles\b', u'naqueles', string)
    string = re.sub(r'\bem aquelas\b', u'naquelas', string)
    string = re.sub(r'\bem aquilo\b', u'naquilo', string)       
    
    #pelo(a), polo(s)  TODOS AMBIGUOS menos pelos!
    string = re.sub(r'\bpor o\b', u'pelo', string)
    string = re.sub(r'\bpor a\b', u'pela', string)
    string = re.sub(r'\bpor os\b', u'pelos', string)
    string = re.sub(r'\bpor as\b', u'pelas', string)
    
    #dentre
    string = re.sub(r'\bde entre\b', u'dentre', string)  

    return string

def testa_substantivo_usuario(request):
    #carrega palavras
    palavras = TestaPalavra.objects.filter(condicao__exact='aguardando')  
    
    for pal in palavras:
        tok = "checks_" + pal.palavra        
        respostas = request.POST.getlist(tok)
        for r in respostas:
            resposta = r
        
        #atualiza resposta
        pal.condicao = 'finalizado'
        pal.resultado = resposta
        pal.save()

        #atualiza lista de substatnivos
        try:
            sub = ListaDeSubstantivos.objects.get(palavra__exact=pal)            
        except:
            sub = ListaDeSubstantivos(palavra=pal.palavra, substantivo=resposta)
            sub.save()              
    
    return selecionar_temas(request)     


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
        parametros = ParametrosDeAjuste(ident=1,k_betweenness=100,f_corte=10,f_min_bigramas=50)
        parametros.save()  
    
    radios_1 = radios_2 = radios_3 = radios_4 = radios_5 = ''
    stringp = parametros.radio_r
    list_par = [int(x) for x in stringp.split(" ")]

    for item in list_par:
        if item == 5:
            radios_1 = 'checked'
        if item == 4:
            radios_2 = 'checked'
        if item == 3:
            radios_3 = 'checked'
        if item == 2:
            radios_4 = 'checked'
        if item == 1:
            radios_5 = 'checked'

    if parametros.permitir_RT == 'sim':
            check_sim = 'checked'
            check_nao = 'off'

    if parametros.permitir_RT == 'nao':
            check_sim = 'off'
            check_nao = 'checked'
    
    if opcao == 'opcao0':    
        novo_parametro = request.POST['valor_k']
        parametros.k_betweenness = int(novo_parametro)
        parametros.save()        
    
    if opcao == 'opcao1':            
        novo_parametro = request.POST['faixa_histo']
        parametros.faixa_histo = float(novo_parametro)
        parametros.save()      
    
    if opcao == 'opcao4':            
        novo_parametro = request.POST['valor_c']
        parametros.corte_n = int(novo_parametro)
        parametros.save() 
    
    if opcao == 'opcao2':            
        novo_parametro = request.POST['valor_fc']
        parametros.f_corte = int(novo_parametro)
        parametros.save()       
    
    if opcao == 'opcao3':            
        novo_parametro = request.POST['valor_fb']
        parametros.f_min_bigramas = int(novo_parametro)
        parametros.save() 
    
    if opcao == 'opcao6':            
        novo_parametro = request.POST['valor_nt']
        parametros.num_tweets = int(novo_parametro)
        parametros.save()

    if opcao == 'opcao7':              
        display_type = request.POST.get("display_type", None)
        parametros.permitir_RT = display_type
        parametros.save()
        if  display_type == 'sim':
            check_sim = 'checked'
            check_nao = 'off'
        if  display_type == 'nao':
            check_sim = 'off'
            check_nao = 'checked'    
    
    if opcao == 'opcao9':
        rad_checked = request.POST.getlist('radios')
        list_check = []
        radios_1 = radios_2 = radios_3 = radios_4 = radios_5 = ''        
        for v in rad_checked:            
            if v == '5':               
                radios_1 = 'checked'
            if v == '4':                
                radios_2 = 'checked'
            if v == '3':                
                radios_3 = 'checked'
            if v == '2':               
                radios_4 = 'checked'
            if v == '1':               
                radios_5 = 'checked'
            list_check.append(v)       
        
        str1 = ' '.join(list_check)
        parametros.radio_r = str1
        parametros.save()   
  
    return render(request, 'extrator/extrator_resultados.html', {'check_sim':check_sim,'check_nao':check_nao,'valorrt':parametros.permitir_RT, 'valornt':parametros.num_tweets,'valork':parametros.k_betweenness, 'valorfc':parametros.f_corte, 'valorfb':parametros.f_min_bigramas, 'xxxx':str(parametros.faixa_histo), 'goto':'ajuste', 'radios_1':radios_1,'radios_2':radios_2,'radios_3':radios_3,'radios_4':radios_4,'radios_5':radios_5, 'valorC':parametros.corte_n})      


def limpar_palavras_ignoradas(request):
    lista = codecs.open("extrator/arquivos/p2_lista_palavrasIgnoradas.txt","w","utf-8")
    lista.write('')
    lista.close()  
    return render(request, 'extrator/extrator_home.html', {})


def carregar_ls(request):    
    arq_subs = codecs.open("extrator/arquivos/lista_de_substantivos.txt", "r", 'utf-8')
    lista_substantivos = arq_subs.readlines() 
    
    lista_obj = []
    for linha in lista_substantivos:
        lista_obj.append(linha)

    #salva dados no BD
    aList = [ListaDeSubstantivos(palavra=l,substantivo='sim') for l in lista_obj]    
    ListaDeSubstantivos.objects.bulk_create(aList) 
    
    return render(request, 'extrator/extrator_resultados.html', {'goto':'ajuste'})


def mostra_resutados(request,passo):            
    if passo == '1':                 
        entrada_original = codecs.open("extrator/arquivos/p1_texto_inicial_original.txt","r", "utf-8")     
        documento = entrada_original.read()
        return render(request, 'extrator/extrator_resultados.html', {'documento':documento,'goto':'resultado-passo-1'})
    
    if passo == '2':
        p2_relatorio = codecs.open("extrator/arquivos/p2_relatorio.txt","r","utf-8").read()       
        return render(request, 'extrator/extrator_resultados.html', {'documento_p2':p2_relatorio,'goto': 'resultado-passo-2'})
    
    if passo == '3':
        do = 'nothing'
        return render(request, 'extrator/extrator_resultados.html', {'rede_p3':'doc','goto': 'resultado-passo-3'})    

    if passo == '4':
        p4_relatorio = codecs.open("extrator/arquivos/p5_relatorio_temas.txt", "r", "utf-8").read()
        return render(request, 'extrator/extrator_resultados.html', {'histo_p4':"hp4",'documento_p4':p4_relatorio,'goto': 'resultado-passo-4-histo'})    

    if passo == '5':
        p5_relatorio = codecs.open("extrator/arquivos/p5_relatorio_temas_subtemas.txt","r","utf-8").read() 
        return render(request, 'extrator/extrator_resultados.html', {'p5_relatorio':p5_relatorio,'resultados_p5':'res','goto':'passo5'})
       
    if passo == '6':
        p6_relatorio = codecs.open("extrator/arquivos/p6_relatorio_final_extracao.txt","r","utf-8").read()             
        return render(request, 'extrator/extrator_resultados.html', {'relatorio_p6':p6_relatorio,'resultados_p6':'res','goto':'p6-result'})

    return render(request, 'extrator/extrator_resultados.html', {})