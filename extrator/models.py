# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TextoPreproc(models.Model):
    vertice = models.CharField('Vertice', max_length=50)
    vertice_num = models.IntegerField()

    def __str__(self):
        return self.vertice

class DadosPreproc(models.Model):
     corretor = models.CharField('Corretor', max_length=10, default='off')
     palavras_texto_original = models.CharField('PalavrasTO', max_length=10)
     palavras_texto_lematizado = models.CharField('PalavrasTL', max_length=10)
     palavras_texto_lematizado_ssw = models.CharField('PalavrasTLSSW', max_length=10)
     quantidade_de_sentencas = models.IntegerField('q_sen')
     palavras_por_sentenca_lssw = models.IntegerField('ppsl')
     palavras_por_sentenca_org = models.IntegerField('ppso')
     nome_rel_protofrase = models.CharField('nome_rel_pfs', max_length=100)     

     def __str__(self):
        return self.palavras_texto_original

class ListaVertices(models.Model):
     node = models.CharField('Node', max_length=50)
     index = models.IntegerField('index', default=-1)

     def __str__(self):
        return self.node

class ListaDeAdjacencias(models.Model):
     vertice_i = models.CharField('vi', max_length=50)
     vertice_f = models.CharField('vf', max_length=50)
     peso = models.IntegerField('peso')

     def __str__(self):
        return self.vertice_i

class TabelaRanking(models.Model):
     vertice_nome =  models.CharField('V_nome', max_length=60)
     vertice_numero = models.IntegerField('V_numero')
     grau = models.IntegerField('Grau')
     grau_norm = models.FloatField('Grau_norm')
     betweenness = models.FloatField('Betweenness')
     betweenness_norm = models.FloatField('Betweenness_norm')
     eigenvector = models.FloatField('eigenvector')
     eigenvector_norm = models.FloatField('eigenvector_norm')
     potenciacao = models.FloatField('potenciação')

     def __str__(self):
        return self.vertice_nome


class TemasNew(models.Model):
    tema = models.TextField('Tema')
    classificacao = models.TextField('Classificacao')
    irt = models.FloatField('IRT Global (%)')   
    
    def __str__(self):
        return self.tema

class SentencasAvaliadas(models.Model):
    tema = models.TextField('Tema')
    subtema = models.TextField('SubTema')
    proto = models.TextField('Proto Frase')
    frase = models.TextField('Frase')
    peso = models.FloatField('peso')
    corte = models.FloatField('corte')
    irse = models.FloatField('IRSE')
    string_graus = models.TextField('Graus da Protofrase')
    

    def __str__(self):
        return self.proto

class TestaPalavra(models.Model):
    palavra  = models.TextField('palavra')
    numero = models.IntegerField('numero')
    condicao = models.TextField('Condicao')
    resultado = models.TextField('Resultado')    

    def __str__(self):
        return self.palavra

class ListaDeSubstantivos(models.Model):
    palavra  = models.TextField('palavra')
    substantivo = models.TextField('Substantivo')
    
    def __str__(self):
        return self.palavra

class ParametrosDeAjuste(models.Model):
    ident = models.IntegerField('Identificacao',default=1)
    k_betweenness = models.IntegerField('K_betweenness',default=100)    
    f_corte = models.IntegerField('Freq_corte_nos_com_dr_min',default=10)
    f_min_bigramas = models.IntegerField('Freq_min_de_bigramas',default=50)   
    num_tweets = models.IntegerField('Número de Tweets',default=100)
    permitir_RT = models.CharField('RT',default=100, max_length=10)    
    faixa_histo = models.FloatField('Faixa',default=0.2)
    exc_cluster = models.IntegerField('Exclusao_de_cluster')
    radio_r = models.TextField('Representatividade_minima', default=0.0)

class CorrigePalavra(models.Model):
    palavra_correta = models.TextField('palavra_correta')
    palavra = models.TextField('palavra')

    def __str__(self):
        return self.palavra


class Clusters(models.Model):
    fim_de_arvore = models.TextField('Cluster Final?')
    etapa = models.IntegerField('Etapa', null=True)
    nucleos = models.TextField('Nucleos')    
    subtemas = models.TextField('Subtemas')
    q_subtemas = models.IntegerField('Qtdd de subtemas', null=True)
    situacao = models.TextField('Situação')
    caminho = models.TextField('Caminho')
    ident = models.TextField('Identificacao')

    def __str__(self):
        return self.nucleos

class MapasTemasESubtemas(models.Model):
    fim_de_arvore = models.TextField('Cluster Final?')
    ident = models.TextField('Id') 
    tema = models.TextField('Tema')
    subtema = models.TextField('Subtema')
    grau = models.FloatField('Grau local')
    irt_l = models.FloatField('IRT local')
    
    def __str__(self):
        return self.tema


class SentencasExtraidas(models.Model):
    ident = models.IntegerField('Ident')
    tema = models.TextField('Tema')
    subtema = models.TextField('SubTema')    
    proto = models.TextField('Proto Frase')
    frase = models.TextField('Frase')
    peso = models.FloatField('peso')
    string_graus = models.TextField('Graus da Protofrase')
    corte = models.FloatField('corte')
    irse = models.FloatField('IRSE')
    representatividade = models.TextField('Representatividade')   

    def __str__(self):
        return self.proto


class SentencasNucleos(models.Model):
    ident = models.IntegerField('Ident')      
    tema = models.TextField('Tema')
    proto = models.TextField('Proto Frase')
    subtema = models.TextField('SubTema') 
    frase = models.TextField('Frase')
    representatividade = models.TextField('Representatividade') 
    peso = models.FloatField('peso')
    string_graus = models.TextField('Graus da Protofrase')
    nucleo = models.TextField('Núcleo da Frase')   

    def __str__(self):
        return self.ident