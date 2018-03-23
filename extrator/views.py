# -*- coding: utf-8 -*-
from __future__ import division
from .models import CorrigePalavra, DadosSelecaoTemas, ParametrosDeAjuste, TextoPreproc, ListaDeSubstantivos, TestaPalavra, DadosPreproc, ListaVertices, TabelaRanking, ListaDeAdjacencias, PesosEAlpha, TemasNew, ProtoFrasesNew, ExtracaoNew, DadosExtracaoNew
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
from operator import itemgetter
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

    #carrega parametros de ajuste
    try:
        parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
        
    except ObjectDoesNotExist:
        parametros = ParametrosDeAjuste(ident=1,k_betweenness=100,dr_delta_min=5,f_corte=10,f_min_bigramas=50,acuidade=100,num_tweets=100)
        parametros.save()
    
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
    
    

    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))   
   
    return render(request, 'extrator/extrator_resultados.html', {'contador_nt':contador_tweets,'tempo_p1dt':tempo_total,'goto':'passo1','muda_logo':'logo_twitter'})


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
    
    #extração de palavras-chave com a tecnica do TextRank
    #print keywords.keywords(documento.encode('utf-8'), language='portuguese')
    
    #tokenizer para Tweets
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
    palavras = tknzr.tokenize(documento)    
      
    for token in palavras: 
        #print repr(token)               
       
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
        DadosPreproc.objects.create(id=1, corretor='off',flag_testapalavra='nao')
   
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p1sd':tempo_total,'goto':'passo1','muda_logo':'logo_salvar_dados'})


def corretor_ortografico(request):
    #inicializa as flags de controle
    r = DadosPreproc.objects.get(id=1)
    r.flag_testapalavra = 'nao'
    r.flag_completo = 'nao'
    r.save()
    
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

        #print repr(palavra)   
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
        
        #buffer1 = list(palavras)
        #buffer1[int(posicao)]=palavra_correta
        #palavras=' '.join(buffer1)        
        #c = 0
        #for ii in palavras.split(' '):            
        #    arq_atualiza.write(ii)            
        #    arq_atualiza.write(' ')
        #    c = c + 1        
        #arq_atualiza.close()
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
    
    #substitui pontuação por ponto final
    texto_inicial = re.sub(r'[!|?|;|.|:|\[|\]]', '.', texto_inicial)
   
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
    
    #Conta o número de sentenças e escreve tokens nos arquivos e substitui pontuação
    sentencas = 0
    for item in tokens:        
        pat = re.compile("[\:\;\.\!\?\-\]\[]+")
        eh = pat.match(item)        
        if eh:
            item = "."
            sentencas = sentencas + 1
        item_l = item.lower()
        
        #elimina todo item que tem o ... do twitter substituindo por um ponto final
        pattern = re.compile(ur'.*…')
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
            if linha[0] != ' ':    
                word_lem = linha.split(' ')[1]
                texto_lematizado.write(word_lem + ' '),
                texto_lematizado_vetor.write(word_lem + '\n'),
                
                #contador de palavras
                pattern = re.compile("(?:[A-Za-z0-9áãõÃÕéóíúàèìòùêâîôûÂÊÎÔÛÁÉÍÓÚÀÈÌÒÙÇç-]+)$") #considera palavra os tokens que contém uma combinação destes caracteres       
                eh_palavra = pattern.match(word_lem.encode('utf-8'))
                if eh_palavra:
                    contador = contador + 1 
     
        except:
            if linha[0] != ' ':    
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
        lista_de_stopwords = arq_stopwords.readlines()
        #stopwords = tokens = nltk.word_tokenize(lista_de_stopwords)
    else:        
        return render(request, 'extrator/extrator_home_2.html', {'dados_de_entrada': None})
    
    stopwords = []
    for linha in lista_de_stopwords:
        stopwords.append(linha.strip())
    
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
        if palavra.strip() not in stopwords:
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
    
    #elimina espaçoes em brannco
    tokens_list = []
    tokens = filter(None, tokens)
    for t in tokens:        
        tokens_list.append(t.strip())    
    tokens_list = filter(None, tokens_list)        
    aList = [TextoPreproc(vertice=token, vertice_num=-1) for token in tokens_list]    
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
            vertices[index] = item.strip()
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
    plt.savefig('extrator/arquivos/p3_rede.png')
    plt.show()
    plt.close()
    
    #finaliza tempo
    #tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    
    return render(request, 'extrator/extrator_resultados.html', {'goto': 'passo3','dados_de_entrada': None, 'relatorio_preproc':None })    


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
    arq_tabela_eigenvector = codecs.open("extrator/arquivos/p4_tabela_eigenvector.txt", 'w','utf-8')
    arq_texto_vertices = codecs.open("extrator/arquivos/p4_texto_vertices.txt", 'w','utf-8')

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
    if parametros.check_grau == 'sim':
        print "calculando métrica graus..."
        tabela_graus = nx.degree(rede, weight='weight')    
        maior_grau = max(tabela_graus.iteritems(), key=operator.itemgetter(1))[1]    
    
    if parametros.check_betw == 'sim':
        print "calculando métrica betweenness..."
        tabela_betweenness = nx.betweenness_centrality(rede, weight='weight', normalized=False, k=int(float(parametros.k_betweenness/100)*len(rede.nodes())))    
        maior_betweenness = max(tabela_betweenness.iteritems(), key=operator.itemgetter(1))[1]
    
    if parametros.check_eigen == 'sim':    
        print "calculando métrica eigenvector..."
        try:
            tabela_eigenvector = nx.eigenvector_centrality(rede)
        except:
            tabela_eigenvector = nx.eigenvector_centrality_numpy(rede)
        maior_eigenvector = max(tabela_eigenvector.iteritems(), key=operator.itemgetter(1))[1] 
   
    
    #cria lista de vertices
    vertices = nx.nodes(rede)

    #gera dicionarios de valores normalizados e cria um texto de vertices (para o próximo passo)
    tabela_grau_normalizado = {}
    tabela_betweenness_normalizado = {}
    tabela_eigenvector_normalizado = {}    
    
    #gera conteudo das tabelas
    for vertice in vertices:        
        arq_texto_vertices.write(vertice + ' ')
        if parametros.check_grau == 'sim':
            tabela_grau_normalizado[vertice] = tabela_graus.get(vertice)/maior_grau
        if parametros.check_betw == 'sim':
            tabela_betweenness_normalizado[vertice] = tabela_betweenness.get(vertice)/maior_betweenness
        if parametros.check_eigen == 'sim':
            tabela_eigenvector_normalizado[vertice] = tabela_eigenvector.get(vertice)/maior_eigenvector
    
      
    for vertice in vertices:        
        arq_texto_vertices.write(vertice + ' ')
        if parametros.check_grau == 'nao':
            tabela_graus[vertice] = 0
            tabela_grau_normalizado[vertice] = 0
        if parametros.check_betw == 'nao':
            tabela_betweenness[vertice] = 0
            tabela_betweenness_normalizado[vertice] = 0
        if parametros.check_eigen == 'nao':
            tabela_eigenvector[vertice] = 0
            tabela_eigenvector_normalizado[vertice] = 0
   
    
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
    
    #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p4cm':tempo_total,'goto': 'passo4', 'muda_logo':'logo_calc_metricas' }) 


def calcula_indice(request):
    #inicia cronometro
    inicio = time.time()
    
    #OBJETIVO: definir a forma de calcular a potenciacao (seus pesos) e gerar a tabela potenciacao
    #matplotlib.use('agg')
    
    #Abre arquivo de dados a serem lidos
    tabela_grau = codecs.open("extrator/arquivos/p4_tabela_graus.txt").readlines()
    tabela_betweenness = codecs.open("extrator/arquivos/p4_tabela_betweenness.txt").readlines()
    tabela_eigenvector = codecs.open("extrator/arquivos/p4_tabela_eigenvector.txt").readlines()
    
    #Carrega dados do BD
    parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)    
    vertices_objs = ListaVertices.objects.all()
    tabela_ranking_completa = TabelaRanking.objects.all()
    try:
        td =  DadosSelecaoTemas.objects.get(id=1)                      
    except:
        DadosSelecaoTemas.objects.create(id=1,p_grau=0,p_bet=0,p_eigen=0)
        td =  DadosSelecaoTemas.objects.get(id=1)
           
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
 
    #Chama função que plota o grafico  
    plota_figura(eixo_y,tabela_potenciacao_ordenada_valores,'black','x','x','x','plota_e_salva_figura_2','extrator/arquivos/p4_grafico_potenciacao.png')   

    arq_tabela_potenciacao.close()
    
    #  #finaliza tempo
    tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    
    return render(request, 'extrator/extrator_resultados.html', {'goto': 'passo4', 'muda_logo':'logo_calc_indice'})


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
            
    #carrega dados
    dados = DadosSelecaoTemas.objects.get(id=1)
    r =  DadosPreproc.objects.get(id=1)
    tabela_bigramas = ListaDeAdjacencias.objects.all()
            
    #inicializa dados do BD
    TemasNew.objects.all().delete()
    
    vertices_objs = ListaVertices.objects.all()
            
    #carrega parametros de ajuste
    try:
        parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
        
    except ObjectDoesNotExist:
        parametros = ParametrosDeAjuste(ident=1,k_betweenness=100,dr_delta_min=5,f_corte=10,f_min_bigramas=50,faixa_histo=0.1)
        parametros.save()

    #print parametros.faixa_histo
            
    #cria arquivo de tabela para histograma
    arq_tabela_histo = codecs.open("extrator/arquivos/p5_tabela_histograma.txt", 'w', 'utf-8')  
    arq_clusters = codecs.open("extrator/arquivos/p5_clusters.txt", 'w', 'utf-8') 
    arq_relatorio = codecs.open("extrator/arquivos/p4_relatorio_temas.txt", 'w')    
      
 

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

    if r.flag_testapalavra.strip() == "nao":    
    
        #print tabela_potenciacao
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
        #print n, bins, patches

        for idx,item in enumerate(n):
            tabela_histograma[bins[idx + 1]] = item
            arq_tabela_histo.write(str(idx) + ' ' + str(bins[idx]) + '->'+  str(bins[idx + 1]) + ' ' + str(item) + '\n')
            
        arq_tabela_histo.close()   
        #print tabela_histograma 
        
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
        #print len(vertices_objs)
        for item in clusters_full.items():
            if len(item[1]) < ((parametros.f_corte)/100)*len(vertices_objs):
                clusters_selecionados[item[0]] = item[1]

            
        #cria lista de vertices selecionados do cluster
        for item in clusters_selecionados.items():
            for linha in item[1]:
                vertices_selecionados[linha.split(' ')[0]] = linha.split(' ')[1]      
            
        #if r.flag_testapalavra.strip() == "nao":
        
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
            
            elif re.compile("[0-9]+").match(palavra):        
                pal.condicao = 'finalizado'
                pal.resultado ='nao'
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

    #print temas_preselecionados



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
        print tema
        tema_entradas = tabela_bigramas.filter(vertice_f=tema)
        peso = 0
    
        print tema_entradas
        for bigrama in tema_entradas:            
            peso = peso + bigrama.peso            
        tabela_graus_entrada[tema] = peso

    print tabela_graus_entrada
    
    # verifica se o grau de entrada do vertice-destino é maior que 50% do peso do bigrama e cria lista de vertices a serem excluidos    
    temas_excluidos = [] 
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
#     arq_lematizador.close()
#     arq_distancias.close()
    
    #lê relatório
    rel_temas = codecs.open("extrator/arquivos/p4_relatorio_temas.txt", 'r', 'utf-8').read()
    
    if r.flag_completo == 'sim':
        return 'none'    
    else: 
        r.flag_testapalavra = 'nao'
        r.save()#         
        #finaliza tempo
        #tempo_total =  ("{0:.4f}".format(time.time() - inicio))                           
        return render(request, 'extrator/extrator_resultados.html', {'tempo_p4st': 'x','goto':'passo4', 'muda_logo':'logo_sel_temas' })

    return render(request, 'extrator/extrator_resultados.html', {'tempo_p4st':'x','goto':'passo4', 'muda_logo':'logo_sel_temas' })
   
##### PASSO 5 ###################################################################################################################################

def processarProtofrases(request):
    #inicia cronometro
    inicio = time.time()

#     #inicializa dados da extrcao
    ExtracaoNew.objects.all().delete()

    #inicializa arquivo do relatório
    arq_procedimento = codecs.open("extrator/arquivos/p5_relatorio_procedimento.txt","w",'utf-8')
   
  
    #carrega arquivos 
    sentencas = codecs.open("extrator/arquivos/p3_texto_sentencas.txt","r",'utf-8').readlines()
    lista_de_adjacencias = codecs.open("extrator/arquivos/p3_lista_adjacencias.txt","r",'utf-8').readlines()
    arq_texto_preprocessado_vet = codecs.open("extrator/arquivos/p2_texto_preprocessado_vetorizado.txt","r",'utf-8').readlines()
    arq_sentencas = codecs.open("extrator/arquivos/p3_texto_sentencas.txt","r",'utf-8').readlines()
    
    #carrega os temas
    temas = TemasNew.objects.all()

    #inicializa listas
    sentencas_avaliadas = OrderedDict()

    #mapeia as sentencas
    sentencas_pp_vet = []
    senten = ''
    for linha in arq_texto_preprocessado_vet:
        if linha.rstrip() != '.':
            senten = senten + ' ' + str(linha.encode('utf-8')).rstrip()
        if linha.rstrip() == '.':
            sentencas_pp_vet.append(senten)
            senten = ''
    #print sentencas_pp_vet

    if len(arq_sentencas) != len(sentencas_pp_vet):
        return render(request, 'extrator/extrator_resultados.html', {'tempo_p5pr':'x','goto': 'passo5', 'muda_logo':'logo_protofrases','mess':'ERRO NA QUANTIDADE DE SENTENCAS' })


    #print len(sentencas)
    #avalia todas as sentenças do texto
    lista_adjacencias = {}
    contador = 0
    for sentenca in sentencas:
        peso = 0
        maior_grau = 0.0
        palavras_sentenca = sentenca.split(' ')
        for i, palavra in enumerate(palavras_sentenca):
            try:
                palavras_sentenca[i+2]                              
                bigrama = palavras_sentenca[i] + ' ' + palavras_sentenca[i+1]
                for linha in lista_de_adjacencias:
                    if bigrama in linha and float(linha.split(' ')[2]) > maior_grau:
                        maior_grau = float(linha.split(' ')[2])              
            except:
                bigrama = 'fim' 
        
        grau_corte = 0.1*maior_grau
        if grau_corte < 1:
            grau_corte = 1.0

  
        corte = 0
        for i, palavra in enumerate(palavras_sentenca):
            try:
                palavras_sentenca[i+2]                              
                bigrama = palavras_sentenca[i] + ' ' + palavras_sentenca[i+1]
                for linha in lista_de_adjacencias:
                    if bigrama in linha:
                        if float(linha.split(' ')[2]) > grau_corte:
                            peso = peso + float(linha.split(' ')[2])
                        else:
                            corte = corte + 1                
            except:
                bigrama = 'fim'     
        sentencas_avaliadas[str(contador) + ' ' + sentenca] = str(peso) + ' ' + str(corte)
        contador = contador + 1
        peso = 0
    print len(sentencas)
    print len(sentencas_avaliadas)    

    #salva dados no BD
    aList = [ExtracaoNew(protofrase=sent[0], frase=sentencas_pp_vet[idx] , peso=sent[1].split(' ')[0] , corte=sent[1].split(' ')[1] , irse=0, irse_p=0, irgs=0 , irgs_p=0) for idx, sent in enumerate(sentencas_avaliadas.items())]    
    ExtracaoNew.objects.bulk_create(aList)    

    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p5pr':'x','goto': 'passo5', 'muda_logo':'logo_protofrases' })


def mapearEextrair(request):
    
    #carrega os temas
    temas = TemasNew.objects.all()

    #carrega frases
    sentencas = ExtracaoNew.objects.all()

    #escreve relatório
    arq_extracao = codecs.open("extrator/arquivos/p5_relatorio_extracao.txt","w",'utf-8')

   
    arq_extracao.write('RELATORIO DE EXTRACAO \n\n')

    for tema in temas:
        arq_extracao.write('Tema: ' + tema.tema + '\n\n')
        arq_extracao.write('protofrase / frase / peso / corte \n\n')
        sentencas1 = ExtracaoNew.objects.filter(protofrase__contains=tema.tema).order_by('-peso','corte')
        for s in sentencas1:
            arq_extracao.write(s.protofrase.rstrip().encode('utf-8').decode('utf-8') + '  /  ' + s.frase.rstrip().encode('utf-8').decode('utf-8') + '  /  ' + str(s.peso) + '  /  ' + str(s.corte) + '\n')
        arq_extracao.write('\n')
    
    #print sentencas1
    arq_extracao.close()
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p5ex':'x','goto':'passo5', 'muda_logo':'logo_map_extracao'})


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
    
    #Calcula as distÂncias relativas entre os vértices da tabela potenciacao
    
    #normalizando os valores
    tabela_graus_ordenada_normalizada = OrderedDict()
    maior_valor = max(tabela_graus_ordenada.iteritems(), key=operator.itemgetter(1))[1]
    
    for k,v in tabela_graus_ordenada.items():        
        tabela_graus_ordenada_normalizada[k] = float(int(v)/int(maior_valor))
    

    #calcula frequencia absoluta de corte    
    f = int(float(parametros.f_corte/100)*len(tabela_graus_ordenada_normalizada))
    
    
    contador = 0
    inicio_cauda = tabela_graus_ordenada_normalizada.keys()[0]
    distancias_relativas_novo =[]
    
    for index, numero in enumerate(tabela_graus_ordenada_normalizada):            
        grau_inicial = tabela_graus_ordenada_normalizada.values()[index]                        
        try:
            grau_final = tabela_graus_ordenada_normalizada.values()[index+1]
        except:
            break             
        #calcula distancia relativa
        dr = 100*((grau_inicial - grau_final)/grau_inicial)
        distancias_relativas_novo.append(dr)
        
        #debugar
        #print str(grau_inicial) + '  ' + str(grau_final) + '  ' + str(dr)
        
        if dr < parametros.dr_delta_min:
            contador += 1
            if contador >= f:
                break
        else:
            inicio_cauda = tabela_graus_ordenada_normalizada.keys()[index+1]
            contador = 0    
    
    #Seleciona região fora da cauda e armazena vertices (nomes e numeros)    
    vertices_selecionados = []
    for key, value in tabela_graus_ordenada_normalizada.items():
        vertices_selecionados.append(key)
        if key == inicio_cauda:
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
    
     #carrega os temas
    temas = TemasNew.objects.all()

    #carrega frases
    sentencas = ExtracaoNew.objects.all()

    #escreve relatório
    arq_extracao = codecs.open("extrator/arquivos/p6_relatorio_final_extracao.txt","w",'utf-8')

    #calcula indice geral de representatividade
    sentenca_maior_peso = ExtracaoNew.objects.order_by('-peso')[0]
    maior_peso = sentenca_maior_peso.peso
  
    for seten in sentencas:
        irgs = (seten.peso - 0.1*seten.corte) / maior_peso
        if irgs < 0:
            irgs = 0
        irgs_por = int(irgs * 100)
        if irgs_por > 80:
            seten.irgs_p = 'alta' 
        if irgs_por > 60 and irgs_por <= 80:
            seten.irgs_p = 'alta-media'
        if irgs_por > 40 and irgs_por <= 60:
            seten.irgs_p = 'media'
        if irgs_por > 20 and irgs_por <= 40:
            seten.irgs_p = 'baixa-media'
        if irgs_por <= 20 :
            seten.irgs_p = 'baixa' 
        
        seten.irgs = irgs
      
        seten.save()

    #calcula indice por tema de representatividade
    for tema in temas:
        sentencas = ExtracaoNew.objects.filter(protofrase__contains=tema.tema)
        sentenca_maior_peso = ExtracaoNew.objects.filter(protofrase__contains=tema.tema).order_by('-peso')[0]
        maior_peso = sentenca_maior_peso.peso
    
        for seten in sentencas:
            irse = (seten.peso - 0.1*seten.corte) / maior_peso
            if irse < 0:
                irse = 0
            irse_por = int(irse * 100)
            if irse_por > 80:
                seten.irse_p = 'alta' 
            if irse_por > 60 and irse_por <= 80:
                seten.irse_p = 'alta-media'
            if irse_por > 40 and irse_por <= 60:
                seten.irse_p = 'media'
            if irse_por > 20 and irse_por <= 40:
                seten.irse_p = 'baixa-media'
            if irse_por <= 20 :
                seten.irse_p = 'baixa'
        
            seten.irse = irse
      
            seten.save()

    
  
    arq_extracao.write('RELATORIO FINAL DE EXTRACAO \n\n')   
    
    arq_extracao.write('1. RANKING GERAL \n\n')   
    arq_extracao.write('frase  \  representatividade \n\n')    
    bag = []
    sentencas = ExtracaoNew.objects.filter(irgs__gt=0.6).order_by('-irgs')
    cont = 1
    for seten in sentencas:                
        if seten.frase not in bag:
            arq_extracao.write(str(cont) + ' - ' + seten.frase.encode('utf-8').decode('utf-8')  + '  \  ' + seten.irgs_p + '\n')
            bag.append(seten.frase)
            cont = cont + 1
   
    arq_extracao.write('\n\n 2. RANKING POR TEMAS \n\n')
    for tema in temas:
        arq_extracao.write('Tema: ' + tema.tema.encode('utf-8').decode('utf-8')  + '\n\n')   
        arq_extracao.write('frase  \  representatividade \n\n')    
        bag = []
        sentencas = ExtracaoNew.objects.filter(protofrase__contains=tema.tema).filter(irse__gt=0.6).order_by('-irse')
        cont = 1
        for seten in sentencas:                
            if seten.frase not in bag:
                arq_extracao.write(str(cont) + ' - ' + seten.frase.encode('utf-8').decode('utf-8')  + '  \  ' + seten.irse_p + '\n')
                bag.append(seten.frase)
                cont = cont + 1
        arq_extracao.write('\n\n')

    arq_extracao.close()    
    





    arq_extracao.close()
    
    return render(request, 'extrator/extrator_resultados.html', {'tempo_p5re':'x','goto':'logo_repres', 'muda_logo':'logo_repres','fim':'fim'})


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
    
    if parametros.check_grau == 'sim':
        check_g = 'checked'
    else:
        check_g = 'off'
    if parametros.check_betw == 'sim':
        check_b = 'checked'
    else:
        check_b = 'off'
    if parametros.check_eigen == 'sim':
        check_c = 'checked'
    else:
        check_c = 'off'        
    
    
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
    
    if opcao == 'opcao8':
        checkeds = request.POST.getlist('checks')
        if 'grau' in checkeds:
            parametros.check_grau = 'sim'
            check_g = 'checked'
        else:
            parametros.check_grau = 'nao'
            check_g = 'off'
        
        if 'betw' in checkeds:
            parametros.check_betw = 'sim'
            check_b = 'checked'
        else:
            parametros.check_betw = 'nao'
            check_b = 'off' 
        
        if 'eigen' in checkeds:
            parametros.check_eigen = 'sim'
            check_c = 'checked'
        else:
            parametros.check_eigen = 'nao'
            check_c = 'off'
        parametros.save()                    

    if opcao == 'opcao4':
        if parametros.check_grau == 'sim':
            check_g = 'checked'
        else:
            check_g = 'off'
        if parametros.check_betw == 'sim':
                    check_b = 'checked'
        else:
            check_b = 'off'
        if parametros.check_eigen == 'sim':
                    check_c = 'checked'
        else:
            check_c = 'off'        
        return render(request, 'extrator/extrator_resultados.html', { 'check_g':check_g,'check_b':check_b,'check_c':check_c,'check_sim':check_sim,'check_nao':check_nao, 'valorrt':parametros.permitir_RT,'valornt':parametros.num_tweets, 'valorae':parametros.acuidade, 'valork':parametros.k_betweenness, 'valordelta':parametros.dr_delta_min, 'valorfc':parametros.f_corte, 'valorfb':parametros.f_min_bigramas, 'xxxx':parametros.faixa_histo,'goto':'ajuste'})

    
  
    return render(request, 'extrator/extrator_resultados.html', {'check_g':check_g,'check_b':check_b,'check_c':check_c,'check_sim':check_sim,'check_nao':check_nao,'valorrt':parametros.permitir_RT, 'valornt':parametros.num_tweets,'valorae':parametros.acuidade, 'valork':parametros.k_betweenness, 'valordelta':parametros.dr_delta_min, 'valorfc':parametros.f_corte, 'valorfb':parametros.f_min_bigramas, 'xxxx':parametros.faixa_histo, 'goto':'ajuste'})      

def resultados(request,arquivo):
    result = DadosPreproc.objects.get(id=1)
    saco = 1   
    if saco == 1: #pura preguiça de tirar a identacao        
        temas = TemasNew.objects.all().values_list('tema', flat=True)
        tabela_graus_n = TabelaRanking.objects.all().values_list('vertice_nome','grau_norm')
        
        #paramentros genericos (raios)
        #raio do esfera parágrafo (deve ser igual ao definido no css)
        raio_par = 15
        raio_maximo_temas = 200
        raio_minimo_temas = 5 
        
        #caclula tamanho do raio do tema central (max 100px) 
        irt_central = TemasNew.objects.get(tema__exact=temas[0])
        diametro_central = int(raio_maximo_temas*irt_central.irt)
        raio_central = int(diametro_central/2)
        tema_central = (temas[0], diametro_central, raio_central, irt_central.irt_p)
        
        #calcula passo angular dos parágrafos do tema central
        tema_central_par = []
        paragrafos = DadosExtracaoNew.objects.filter(tema__exact=temas[0])
        delta = int(180/len(paragrafos))
        posicao = 0
        
        #calcula distAncias do centro do tema central ate o centro dos parágrafos       
        bias_central = 0        
        for paragrafo in paragrafos:
            if paragrafo.protofrase.strip() != 'tema nao convergiu':
                distancia = int(tema_central[2] + raio_par + (100 - paragrafo.irse_p))             
                if distancia > bias_central:
                    bias_central = distancia
                pos_x = int(distancia*math.cos(math.radians(posicao)))
                pos_y = int(distancia*math.sin(math.radians(posicao)))
                posicao = posicao + delta
                nome = (temas[0] + str(pos_x) + str(pos_y))
                tema_central_par.append((temas[0], pos_x, pos_y, paragrafo.sentenca, nome, paragrafo.irse_p ))   
        
        # CALCULO DO BIAS ###############################################################################
        #acha maior distancia entre subtema e paragrafo (bias_subtema)
        # bias_subtema = 0
        # vet_buf = []
        # for i in xrange(1, len(temas)):            
        #     #calcula parametros
        #     tema = TabelaRanking.objects.get(vertice_nome__exact=temas[i])
        #     irt = TemasNew.objects.get(tema__exact=temas[i])
        #     diametro_vertice = int(raio_vertices*irt.irt)
        #     raio_vertice = int(diametro_vertice/2)
        #     vet_buf.append((temas[i],raio_vertice))        
        
        # for tema in temas:
        #     paragrafos = DadosExtracaoNew.objects.filter(tema__exact=tema)       
        #     for paragrafo in paragrafos:
        #         if paragrafo.protofrase.strip() != 'tema nao convergiu':
        #             distancia = 0
        #             for vetor in vet_buf:
        #                 if vetor[0] == tema:
        #                     distancia = int(vetor[1] + raio_par + 80*(1-paragrafo.irse))
        #                     if distancia > bias_subtema:
        #                         bias_subtema = distancia

        # bias = bias_central + bias_subtema
        # if not paragrafos:
        #     bias = 100             
        ##########################################################################################        
        
        #Define os angulos dos temas e inicializa vetor
        delta_grau = float(360/(len(temas) - 1))    
        grau = delta_grau
        vetor_temas =[]   
        
        #menor distancia do subtema ao raio centrol
        distancia_do_centro = 330 #raio max central, diametro paragrafo, distancia máxima tema-paragrafo
        
        # #menor raio
        # t = TemasNew.objects.all()
        # diametro_2_vertice = int(raio_vertices*t[1].irt)
        # raio_2_vertice = int(diametro_2_vertice/2)
        # menor_distancia_do_tema = raio_central + raio_2_vertice + bias + 10
        # tem = TabelaRanking.objects.get(vertice_nome__exact=t[1].tema)
        
        # distancia_do_centro = int(menor_distancia_do_tema/(1 - tem.grau_norm)) 
        
        for i in xrange(1, len(temas)):
            
            #calcula parametros
            tema = TabelaRanking.objects.get(vertice_nome__exact=temas[i])
            irt = TemasNew.objects.get(tema__exact=temas[i])
            diametro_vertice = int(raio_maximo_temas*irt.irt)
            raio_vertice = int(diametro_vertice/2)
            distancia_centro = distancia_do_centro + (200 - 200*(tema.grau_norm))
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
                            distancia = int(vetor[5] + raio_par + (100 - paragrafo.irse_p))                                      
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


# def calcula_indice(request):
#     #inicia cronometro
#     inicio = time.time()
    
#     #OBJETIVO: definir a forma de calcular a potenciacao (seus pesos) e gerar a tabela potenciacao
#     matplotlib.use('agg')
    
#     #Abre arquivo de dados a serem lidos
#     tabela_grau = codecs.open("extrator/arquivos/p4_tabela_graus.txt").readlines()
#     tabela_betweenness = codecs.open("extrator/arquivos/p4_tabela_betweenness.txt").readlines()
#     tabela_eigenvector = codecs.open("extrator/arquivos/p4_tabela_eigenvector.txt").readlines()
    
#     #Carrega dados do BD
#     parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)
    
#     vertices_objs = ListaVertices.objects.all()

#     tabela_ranking_completa = TabelaRanking.objects.all()
#     try:
#         td =  DadosSelecaoTemas.objects.get(id=1)                      
#     except:
#         DadosSelecaoTemas.objects.create(id=1,p_grau=0,p_bet=0,p_eigen=0)
#         td =  DadosSelecaoTemas.objects.get(id=1)
           
#     #Inicializa arquivos a serem escritos
#     arq_tabela_potenciacao = codecs.open("extrator/arquivos/p4_tabela_potenciacao.txt", 'w', 'utf-8')    
#     arq_matriz_pesos = codecs.open("extrator/arquivos/p4_matriz_pesos.txt", 'w', 'utf-8')
#     arq_relatorio = codecs.open("extrator/arquivos/p4_relatorio_potenciacao.txt", 'w')   
   
#     #Prepara o BD para receber os novos pesos
#     pesos = PesosEAlpha.objects.all()
#     pesos.delete()
    
#     #gera matriz de pesos para cada caso
#     #var = 0.05
#     #if parametros.check_grau == 'sim' and parametros.check_betw == 'sim' and parametros.check_eigen == 'sim': 
       
#     #    for a1 in range(0,20):
#     #        for a2 in range(0,20):
#     #            a3 = 20 - a1 - a2                
#     #            arq_matriz_pesos.write(str(a1*var) + ' ')
#     #            arq_matriz_pesos.write(str(a2*var) + ' ')
#     #            arq_matriz_pesos.write(str(a3*var) + ' ')
#     #            arq_matriz_pesos.write('\n')
#     #    arq_matriz_pesos.close()
    
#     #gera matriz de pesos para cada caso
#     var = 0.1
#     if parametros.check_grau == 'sim' and parametros.check_betw == 'sim' and parametros.check_eigen == 'sim': 
       
#         for a1 in range(0,12):
#             for a2 in range(0,12):
#                 a3 = 10 - a1 - a2
#                 if a3 >= 0 and a1 != 0 and a2 != 0 and a3 != 0:
#                     arq_matriz_pesos.write(str(a1*var) + ' ')
#                     arq_matriz_pesos.write(str(a2*var) + ' ')
#                     arq_matriz_pesos.write(str(a3*var) + ' ')
#                     arq_matriz_pesos.write('\n')
#         arq_matriz_pesos.close()
    
#     if parametros.check_grau == 'sim' and parametros.check_betw == 'nao' and parametros.check_eigen == 'nao':
#         arq_matriz_pesos.write(str(1.0) + ' ' + str(0.0) + ' ' + str(0.0) + '\n')
#         arq_matriz_pesos.close()
    
#     if parametros.check_grau == 'nao' and parametros.check_betw == 'sim' and parametros.check_eigen == 'nao': 
#         arq_matriz_pesos.write(str(0.0) + ' ' + str(1.0) + ' ' + str(0.0) + '\n')
#         arq_matriz_pesos.close()
    
#     if parametros.check_grau == 'nao' and parametros.check_betw == 'nao' and parametros.check_eigen == 'sim':
#         arq_matriz_pesos.write(str(0.0) + ' ' + str(0.0) + ' ' + str(1.0) + '\n')
#         arq_matriz_pesos.close()
    
#     if parametros.check_grau == 'sim' and parametros.check_betw == 'sim' and parametros.check_eigen == 'nao':
#         for a1 in range(1,10):
#             p1 = a1*var
#             p2 = 1 - p1
#             arq_matriz_pesos.write(str(p1) + ' ' + str(p2) + ' ' + str(0.0) + '\n')       
#         arq_matriz_pesos.close()
    
#     if parametros.check_grau == 'sim' and parametros.check_betw == 'nao' and parametros.check_eigen == 'sim':
#         for a1 in range(1,10):
#             p1 = a1*var
#             p2 = 1 - p1
#             arq_matriz_pesos.write(str(p1) + ' ' + str(0.0) + ' ' + str(p2) + '\n')       
#         arq_matriz_pesos.close()
    
#     if parametros.check_grau == 'nao' and parametros.check_betw == 'sim' and parametros.check_eigen == 'sim':
#         for a1 in range(1,10):
#             p1 = a1*var
#             p2 = 1 - p1
#             arq_matriz_pesos.write(str(0.0) + ' ' + str(p1) + ' ' + str(p2) + '\n')       
#         arq_matriz_pesos.close()
    
#     ## FIM ETAPA 2 ####################################################
#     ## ETAPA 3: SELEÇÃO DOS PESOS DAS MÉTRICAS ########################

#     # abre matriz de pesos
#     pesos = codecs.open("extrator/arquivos/p4_matriz_pesos.txt").readlines()

#     #inicializa matlibplot para duas figuras e cores
#     rgb_a=5
#     rgb_b=94
#     rgb_c=200

#     #calculo de alpha para cada conjunto de peso
#     for peso in pesos:
#         pgra = float(peso.split(' ')[0])
#         pbet =  float(peso.split(' ')[1])
#         peigen = float(peso.split(' ')[2])

#         # CALCULA POTENCIAÇÃO
#         tabela_potenciacao_temp = {}
#         for vertice in vertices_objs:
#             grau_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).grau_norm
#             bet_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).betweenness_norm
#             eigen_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).eigenvector_norm
#             potenciacao = float(pgra)*float(grau_n) + float(pbet)*float(bet_n) + float(peigen)*float(eigen_n)
#             tabela_potenciacao_temp[vertice.node] = potenciacao
        
#         # Cria uma tabela vertice(nome)-indice
#         tabela_potenciacao_temp_ordenada = {}
#         tabela_potenciacao_temp_ordenada = sorted(tabela_potenciacao_temp.items(),key=lambda x: x[1], reverse=True)

#         # exclui os 5% ultimos temas quando pertinente (n>0)
#         corte = 0.00
#         numero_vertices_excluidos = int(corte*len(tabela_potenciacao_temp_ordenada))
#         if numero_vertices_excluidos > 0:            
#             del tabela_potenciacao_temp_ordenada[-numero_vertices_excluidos:]
        
#         #exclui vertice de indice zero       
#         flag = 'on'
#         while flag == 'on':        
#             for i,v in enumerate(tabela_potenciacao_temp_ordenada):
#                 flag = 'off'
#                 if v[1] == 0.0:
#                     flag = 'on'
#             if flag == 'on':
#                 del tabela_potenciacao_temp_ordenada[-1:]

#         #Faz a regressão linear e calcula alpha da tabela
#         valores_potenciacao = [valor[1] for valor in tabela_potenciacao_temp_ordenada]  
#         print valores_potenciacao      
#         fit = powerlaw.Fit(valores_potenciacao, discrete=True)
#         print fit.xmin

#         data = valores_potenciacao
#         ####
#         figPDF = powerlaw.plot_pdf(data, color='b')
#         powerlaw.plot_pdf(data, linear_bins=True, color='r', ax=figPDF)
#         ####
#         figPDF.set_ylabel("p(X)")
#         figPDF.set_xlabel(r"Word Frequency")
#         figname = 'FigPDF'
#         pylab.savefig('extrator/arquivos/teste.png', bbox_inches='tight',  dpi=300)
#         #savefig(figname+'.tiff', bbox_inches='tight', dpi=300)

        

       
#         #calcula o MLF dos dados (o quão ajustados estão)
#         # maximum likelihood fitting (MLF)
#         soma = 0
#         for p in valores_potenciacao:
#             soma = soma + log(float(p)/float(fit.xmin))
#         alpha_esperado = -1*(1 + len(tabela_potenciacao_temp_ordenada)*(1.0/soma))
        
#         # Caclula o erro entre alpha e MLF
#         erro = (abs(fit.alpha - alpha_esperado)/fit.alpha)*100
    
#         #plota gráfico
#         eixo_y = list(range(len(tabela_potenciacao_temp_ordenada)))
        
#         #CHAMA FUNÇÃO QUE PLOTA FIGURAS
#         plota_figura(eixo_y,valores_potenciacao,rgb_a,rgb_b,rgb_c,fit.alpha,'plota_figura_1','endereco')        
        
#         #_test_chart(eixo_y,valores_potenciacao,rgb_a,rgb_b,rgb_c,fit.alpha,'plota_figura_1','endereco')       
#         rgb_a = (rgb_a + 50)%255
#         rgb_b = (rgb_b + 10)%255
#         rgb_c = (rgb_c+ 80)%255
    
#         #armazena os pesos, alpha, MLF e erro no BD
#         resultado = PesosEAlpha(p_grau = pgra , p_betw = pbet, p_eigene = peigen , alpha = fit.alpha, alphaesp = alpha_esperado, erro = erro)
#         resultado.save()        

#     #CHAMA FUNÇÃO QUE SALVA FIGURAS   
#     plota_figura('x','x','x','x','x','x','salva_figura_1','extrator/arquivos/p4_grafico_alphas.png')    
  
#     #Busca pesos de menor erro e maior valor alpha ( para erro < 1%)
#     corte_erro = 0
#     pesos_selecionados = []
#     while not pesos_selecionados:
#         lista_de_erros = []
#         lista_de_erros = PesosEAlpha.objects.all().filter(erro__lt=corte_erro).order_by('alpha')
#         pesos_selecionados = lista_de_erros.last()
#         corte_erro = corte_erro + 1
#         if pesos_selecionados:
#             corte_erro = corte_erro - 1

#     #salvar dados com parÂmetros escolhidos
#     td.p_grau= pesos_selecionados.p_grau 
#     td.p_eigen= pesos_selecionados.p_eigene
#     td.p_bet = pesos_selecionados.p_betw
#     td.save()

#     #Monta a Tabela de Indices com o Peso encontrado e salva no BD
#     pgra =  pesos_selecionados.p_grau
#     pbet =   pesos_selecionados.p_betw
#     peigen =  pesos_selecionados.p_eigene

#     #CALCULA POTENCIAÇÃO
#     tabela_potenciacao_temp = {}
#     for vertice in vertices_objs:
#         grau_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).grau_norm
#         bet_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).betweenness_norm
#         eigen_n = tabela_ranking_completa.get(vertice_nome__exact=vertice.node).eigenvector_norm
#         potenciacao = float(pgra)*float(grau_n) + float(pbet)*float(bet_n) + float(peigen)*float(eigen_n)
             
#         #Salva na Tabela Ranking
#         tabela = TabelaRanking.objects.get(vertice_nome__iexact = vertice.node)
#         tabela.potenciacao = potenciacao
#         tabela.save()    

#     #salva a tabela de indice em um arquivo em ordem alfabética e cria figura
#     tabela_potenciacao_ordenada = TabelaRanking.objects.all().order_by('-potenciacao')
#     tabela_potenciacao_ordenada_valores = []
#     eixo_y = list(range(len(tabela_potenciacao_ordenada)))   
    
#     for linha in tabela_potenciacao_ordenada:        
#         index = ListaVertices.objects.get(node__exact=linha.vertice_nome).index
#         arq_tabela_potenciacao.write(str(index) + ' ' + linha.vertice_nome + ' ' + str(linha.potenciacao) + ' ' + '\n')        
#         tabela_potenciacao_ordenada_valores.append(linha.potenciacao)
 
#     #Chama função que plota o grafico  
#     plota_figura(eixo_y,tabela_potenciacao_ordenada_valores,'black','x','x','x','plota_e_salva_figura_2','extrator/arquivos/p4_grafico_alpha_selecionado.png')   

#     ## FIM ETAPA 3 #######################################################
#     ## GERA RELATÒRIO ####################################################
   
#     arq_relatorio.write('RELATÓRIO FINAL - TABELA ÍNDICE\n\n\n')   
#     arq_relatorio.write('ETAPA 1 - DETERMINANDO OS PESOS DAS MÉTRICAS\n')
#     arq_relatorio.write('   - Método: Melhor ajuste à Lei da Potência\n')
#     arq_relatorio.write('   - Entrada: Matriz de pesos-candidato\n')
#     arq_relatorio.write('              Variação: 0.1 à 0.9 em ' + str(var) + '\n')
#     arq_relatorio.write('              Restrição: soma dos pesos = 1\n\n')
#     arq_relatorio.write('   - Ajuste à lei de potência\n')
#     arq_relatorio.write('              Dados: Exclui os ' + str(corte*100) + '% últimos vértices - ' +  str(numero_vertices_excluidos) + ' vértices.\n')
#     arq_relatorio.write('              Cálculo de Alpha: Métodos dos mínimos quadrados\n')
#     arq_relatorio.write('              Alpha de ajuste:: Maximun Likelihood fitting\n')
#     arq_relatorio.write('              Erro = |alpha de ajuste - alpha| \n\n')
#     arq_relatorio.write('   - Resultado\n')
#     arq_relatorio.write('              Alpha / Alpha de ajuste / erro (%) / Pesos \n')
#     lista_de_alphas = PesosEAlpha.objects.all().order_by('alpha')
#     for la in lista_de_alphas:
#         arq_relatorio.write('              ' + str(la.alpha) + ' / ' + str(la.alphaesp) + ' / ' + str(la.erro) + ' / ' + str(la.p_grau) + ' ' + str(la.p_betw) + ' ' + str(la.p_eigene) + ' \n')
#     arq_relatorio.write('\n              Corte: erro > ' + str(corte_erro) + ' % \n\n')
#     arq_relatorio.write('              Alpha / Alpha de ajuste / erro (%) / Pesos \n')
#     for li in lista_de_erros:
#         arq_relatorio.write('              ' + str(li.alpha) + ' / ' + str(li.alphaesp) + ' / ' + str(li.erro) + ' / ' + str(li.p_grau) + ' ' + str(li.p_betw) + ' ' + str(li.p_eigene) + ' \n')
#     arq_relatorio.write('\n              Maior alpha: ' + str(pesos_selecionados.alpha) + ' \n')
#     arq_relatorio.write('              Pesos selecionados: Graus: ' + str(pesos_selecionados.p_grau) + ' ; Betweeness: ' + str(pesos_selecionados.p_betw) + ' ; eigenvector: ' + str(pesos_selecionados.p_eigene) + ' \n\n')
#     arq_relatorio.write('ETAPA 2 - TABELA RANKING\n')
#     arq_relatorio.write('   palavra - índice\n\n')
#     for linha in tabela_potenciacao_ordenada:
#         arq_relatorio.write(linha.vertice_nome.encode('utf-8') + ' - ' + str(linha.potenciacao) + '\n')

#     #fecha arquivos
#     arq_relatorio.close()
#     arq_tabela_potenciacao.close()
    
#     rel_ind = codecs.open("extrator/arquivos/p4_relatorio_potenciacao.txt","r",'utf-8').read()
    
#      #finaliza tempo
#     tempo_total =  ("{0:.4f}".format(time.time() - inicio))  
    
#     return render(request, 'extrator/extrator_resultados.html', {'tempo_p4ci':tempo_total,'goto': 'passo4', 'muda_logo':'logo_calc_indice'})

# def processarProtofrases(request):
#             #inicia cronometro
#     inicio = time.time()

#     #carrega parâmetros
#     parametros = ParametrosDeAjuste.objects.get(ident__iexact=1)        

#     #inicializa arquivo do relatório
#     arq_procedimento = codecs.open("extrator/arquivos/p5_relatorio_procedimento.txt","w",'utf-8')
#     arq_extracao = codecs.open("extrator/arquivos/p5_relatorio_extracao.txt","w",'utf-8')

#     #Inicializa BD de frases
#     ExtracaoNew.objects.all().delete()
    
#     #carrega protofrases
#     temas = TemasNew.objects.all()
#     buffer_temas = []

#     #Carrega texto lematizado
#     tokens = TextoPreproc.objects.all()

#     #gera arquivo do sub-docimento
#     arq_subdocumento = codecs.open("extrator/arquivos/p5_texto_sub_preprocessado_sentencas.txt",'w','utf-8')
    
#     for token in tokens:       
#         if token.vertice == '.':
#             arq_subdocumento.write('\n')
#         else:
#             arq_subdocumento.write(token.vertice)
#             arq_subdocumento.write(' ')
#     arq_subdocumento.close()

#     #inicia analise de cada tema
#     for tema in temas:        
#         print ('processando o tema ' + tema.tema.encode('utf-8') + '...')
        
#         #inicia relatórios
#         arq_procedimento.write('TEMA: ' + tema.tema + '\n\n')
#         arq_extracao.write('TEMA: ' + tema.tema + '\n\n')

#         #armazena tema no BD de protofrases
#         ProtoFrasesNew.objects.all().delete()
#         pf = ProtoFrasesNew(protofrase = tema.tema, extracao='nao',frase='null')
#         pf.save()
                
#         #flag de termino do procedomemto (off)
#         flag = 'on'
#         iteracao = 0
#         convergiu_tema = 'nao'
#         extracao = []      
        
#         while flag == 'on': 
            
#             print "carregando protofrases"
#             #testa se todas as PFs já extrairam frases
#             protofrases = ProtoFrasesNew.objects.filter(extracao = 'nao')
#             if not protofrases:
#                 flag = 'off'                 
#                 break
#             flag = 'on'   
            
#             #relatório                       
#             arq_procedimento.write(' - ITERACAO ' + str(iteracao) + ':\n' + '          proto-frase / tamanho da rede (sentencas) / extraiu?\n ')    
           
#             #avalia as protofrases que ainda nao obtiveram extracao
#             buffer_pfs = []
#             pfn = 0
#             memoria_pf = []
#             memoria_st = []
#             indx = 0
            
#             for protofrase in protofrases:
                
#                 print ('protofrase ' + str(pfn))                
                
#                 #separa palavras da protofrase e armazena em uma lista e atualiza subtenas
#                 palavras = protofrase.protofrase.split(' ')
#                 subtemas_pre_selecionados = []
                
#                 #reinicializa flag
#                 convergiu_tema = 'nao'
             
#                 #gera sub-documento e recebe o numero de sentencas
#                 numero_de_sentencas, seten, sentencas = GeraSubDocumento(palavras)                
               
#                 #relatorio
#                 arq_procedimento.write('       '  + protofrase.protofrase + '     /     ' + str(numero_de_sentencas) + '    /    ')                  
                
#                 #print 'armazena protofrases e extração...'
#                 if numero_de_sentencas == 1:
#                     convergiu_tema = 'sim'
#                     frase = codecs.open('extrator/arquivos/p5_texto_tema.txt','r','utf-8').readlines()                  
#                     extracao.append((tema.tema, protofrase.protofrase,frase[0].strip()))
#                     arq_extracao.write(protofrase.protofrase + '      ' + frase[0] + '\n')
#                     arq_procedimento.write('sim' + '\n')
#                     pfn += 1
#                 else:                  
#                     #Se o conjunto de palavras da pf já foi executado, pega o resultado
#                     if set(palavras) in memoria_pf:
#                         ind = memoria_pf.index(set(palavras))                                    
#                         subtemas_pre_selecionados = memoria_pf[ind] 
#                     #senão, chama algoritmo de seleção de temas  
#                     else:                                
                      
#                         #gera nova rede
#                         tgo = GeraRede(request)
                       
#                         #seleciona os subtemas
#                         subtemas_pre_selecionados = SelecionaSubTemas(tgo)
                      
#                         #atualiza memória de execuções   
#                         memoria_pf.append(set(palavras))
#                         memoria_st.append(set(subtemas_pre_selecionados))
                    
#                     #print subtemas_pre_selecionados
#                     #adiciona novas protofrases no buffer 
#                     convergiu = 'nao'                   
#                     for subtema in subtemas_pre_selecionados:
#                         if subtema not in palavras:
#                             ultimo_tema = palavras[-1]
#                             bigramas = ListaDeAdjacencias.objects.filter(vertice_i__exact=ultimo_tema)
#                             possiveis_subtemas = bigramas.values_list('vertice_f', flat=True)                         
#                             #só acrescenta subtema se ele for vertice de entrada da ultima palavra da protofrase
#                             if subtema in list(possiveis_subtemas):
#                                 convergiu = 'sim'
#                                 pf_i = ' '.join(palavras)
#                                 pf = pf_i + ' ' + subtema
#                                 buffer_pfs.append(pf)                               
#                     if convergiu == 'nao':                       
#                         set_count = Counter(elem for elem in sentencas)                        
#                         soma = sum(set_count.values())
#                         for k,v in set_count.items():
#                             per = int((float(v)/soma)*100)
#                             if per >= parametros.acuidade:
#                                 convergiu_tema = 'sim'
#                                 arq_procedimento.write('sim - com repeticao' + '\n')
#                                 frase = codecs.open('extrator/arquivos/p5_texto_tema.txt','r','utf-8').readlines()                  
#                                 extracao.append((tema.tema, protofrase.protofrase,frase[0].strip()))
#                                 arq_extracao.write(protofrase.protofrase + '      ' + frase[0] + '\n')  
#                         if convergiu_tema == 'nao':                              
#                             arq_procedimento.write('null' + '\n') 
#                     else:
#                         arq_procedimento.write(protofrase.extracao + '\n')                               
#                     pfn += 1     

#             print 'atualizando banco de dados...'

#             #atualiza protofrases no BD
#             arq_procedimento.write('\n\n\n')
#             iteracao +=1
#             print ('Iteração ' + str(iteracao) )
#             if buffer_pfs:
#                 ProtoFrasesNew.objects.all().delete()
#                 aList = [ProtoFrasesNew(protofrase=pf, extracao='nao',frase='null') for pf in buffer_pfs]    
#                 ProtoFrasesNew.objects.bulk_create(aList)
#             else:
#                 ProtoFrasesNew.objects.all().delete()
                            
        
#         if convergiu_tema == 'nao':
#             f = ExtracaoNew(tema = tema.tema, protofrase = 'tema nao convergiu', frase = 'tema nao convergiu')
#             f.save()

#         else:           
#             aList = [ExtracaoNew(tema = linha[0], protofrase = linha[1] , frase = linha[2] ) for linha in extracao]    
#             ExtracaoNew.objects.bulk_create(aList)
        
#         arq_procedimento.write('\n\n\n')
#         arq_extracao.write('\n\n\n')      
    
#     #fecha arquivos
#     arq_procedimento.close()
#     arq_extracao.close()

#     rel_proc = codecs.open("extrator/arquivos/p5_relatorio_procedimento.txt", 'r','utf-8').read()
     
#     #finaliza tempo
#     tempo_total =  ("{0:.4f}".format(time.time() - inicio))
    
#     return render(request, 'extrator/extrator_resultados.html', {'tempo_p5pr':tempo_total,'goto': 'passo5', 'muda_logo':'logo_protofrases' })


# def mapearEextrair(request):
#     #inicia cronometro
#     inicio = time.time()

#     #relatorio
#     arq_relatorio =codecs.open("extrator/arquivos/p5_relatorio_extracao.txt","w")

#     #carrega arquivos
#     arq_texto_lematizado = codecs.open("extrator/arquivos/p2_texto_lematizado_ssw.txt","r",'utf-8')
#     arq_texto_preprocessado = codecs.open("extrator/arquivos/p2_texto_preprocessado.txt","r",'utf-8')
    
#     #carrega os temas
#     temas = TemasNew.objects.all()

#     #inicializa dados da extrcao
#     DadosExtracaoNew.objects.all().delete()
    
#     #Verifica as repetições de cada protofrase
#     for tema in temas:
#         frases = Counter(ExtracaoNew.objects.filter(tema = tema.tema).values_list('frase', flat=True))        
#         aList = [DadosExtracaoNew(irgs=0,irgs_p=0,irse=0,irse_p=0,tema=tema.tema, protofrase = key, quantidade = value) for key,value in frases.items()]    
#         DadosExtracaoNew.objects.bulk_create(aList)   
            
#     #Prepara textos do mapeamento separando as sentencas e tirando os espacoes em branco do começo e do fim (strip)
#     sentencas_lem_strip = []
#     texto_lematizado = arq_texto_lematizado.read()
#     sentencas_lem = texto_lematizado.split('.')
#     for sentenca in sentencas_lem:
#         sentencas_lem_strip.append(sentenca.strip())
          
#     sentencas_pp_strip = [] 
#     texto_preprocessado = arq_texto_preprocessado.read()
#     sentencas_pp = texto_preprocessado.split('.') 
#     for sentenca in sentencas_pp:
#         sentencas_pp_strip.append(sentenca.strip())
   
#     #teste de mapeamento
#     if len(sentencas_lem) != len(sentencas_pp):       
#         return render(request, 'extrator/extrator_resultados.html', {'goto':'passo5', 'muda_logo_error':'logo_map_extracao' })

#     #inicializa relatorio
#     arq_relatorio.write('   RELATÓRIO DE EXTRAÇÃO\n\n\n  tema   /   frase   /   repetições   /   sentença (texto original)\n\n')

#     dados = DadosExtracaoNew.objects.all()

#     for dado in dados:
      
#         try:        
#             indice =  sentencas_lem_strip.index(dado.protofrase.strip())
#             dado.sentenca = sentencas_pp_strip[indice].strip()
#             dado.save()
#             arq_relatorio.write('  ' + dado.tema.encode('utf-8') + '  /  ' + dado.protofrase.encode('utf-8') + '  /  ' + str(dado.quantidade) + '  /  ' + dado.sentenca.encode('utf-8') + '\n')
#         except:
#             dado.sentenca = 'null - nao convergiu'
#             dado.save()
#             arq_relatorio.write('  ' + dado.tema.encode('utf-8') + '  /  ' + dado.protofrase.encode('utf-8') + '  /  ' + str(dado.quantidade) + '  /  ' + dado.sentenca.encode('utf-8') + '\n')

#     arq_relatorio.close()

#     rel_ext = codecs.open("extrator/arquivos/p5_relatorio_extracao.txt", 'r','utf-8').read()
         
#     #finaliza tempo
#     tempo_total =  ("{0:.4f}".format(time.time() - inicio))
    
#     return render(request, 'extrator/extrator_resultados.html', {'tempo_p5ex':tempo_total,'goto':'passo5', 'muda_logo':'logo_map_extracao'})

