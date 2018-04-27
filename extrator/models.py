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
     flag_testapalavra = models.TextField('Flag -Testa Substantivo')    
     flag_completo = models.TextField('Flag - Exec. Completa')
     

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
#     betweenness = models.DecimalField('Betweenness',max_digits=10, decimal_places=5)
#     eigenvector = models.DecimalField('eigenvector',max_digits=10, decimal_places=5)

     def __str__(self):
        return self.vertice_nome


class DadosSelecaoTemas(models.Model):   
    p_grau = models.FloatField('Peso Graus')
    p_eigen = models.FloatField('Peso Betweeness')
    p_bet = models.FloatField('Peso eigenvector')
    sel_graus = models.CharField('Graus?',default='sim', max_length=10)
    sel_betw = models.CharField('Betwweeness?',default='sim', max_length=10)
    sel_eigen = models.CharField('eigenvector?',default='sim', max_length=10)   

    def __str__(self):
        return self.temas_selecionados



class PesosEAlpha(models.Model):
    p_grau = models.FloatField('Peso_Grau')
    p_betw = models.FloatField('Peso_Betweenness')
    p_eigene = models.FloatField('Peso_eigenvector')
    alpha = models.FloatField('Alpha')
    alphaesp = models.FloatField('Alphaesp')
    erro = models.FloatField('erro')


    def __str__(self):
        return self.alpha

class TemasNew(models.Model):
    tema = models.TextField('Tema')
    classificacao = models.TextField('Classificacao')
    irt = models.FloatField('IRT Global (%)')
    irt_l = models.FloatField('IRT Local (Sem referência)')
    
    def __str__(self):
        return self.tema

class ProtoFrasesNew(models.Model):
    protofrase = models.TextField('Proto Frase')
    extracao = models.TextField('Extraiu?',default='nao')
    frase = models.TextField('Frase extraida')

    def __str__(self):
        return self.protofrase

class ExtracaoNew(models.Model):
    protofrase = models.TextField('Proto Frase')
    frase = models.TextField('Frase')
    peso = models.FloatField('peso')
    corte = models.FloatField('corte')
    irse = models.FloatField('IRSE')
    rep_tema = models.TextField('Representativadade_tema')    
    irgs = models.FloatField('IRGS')     
    rep_geral = models.TextField('Representatividade_geral')

    

    def __str__(self):
        return self.protofrase

class DadosExtracaoNew(models.Model):
    tema  = models.TextField('Tema')
    protofrase = models.TextField('Proto Frase')
    quantidade = models.IntegerField('Quantidade')
    sentenca = models.TextField('Sentenca')
    irse = models.FloatField('IRSE')
    irse_p = models.FloatField('IRSE%')
    #rep_tema = models.TextField('Representativadade_tema')    
    irgs = models.FloatField('IRGS') 
    irgs_p = models.FloatField('IRGS%')
    
    #rep_geral = models.TextField('Representatividade_geral')

    def __str__(self):
        return self.tema

class TestaPalavra(models.Model):
    palavra  = models.TextField('palavra')
    numero = models.IntegerField('nnumero')
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
    dr_delta_min = models.IntegerField('Delta_distancia_relativa_min',default=5)
    f_corte = models.IntegerField('Freq_corte_nos_com_dr_min',default=10)
    f_min_bigramas = models.IntegerField('Freq_min_de_bigramas',default=50)
    acuidade = models.IntegerField('Freq_min_de_bigramas',default=100)
    num_tweets = models.IntegerField('Número de Tweets',default=100)
    permitir_RT = models.CharField('RT',default=100, max_length=10)
    check_grau = models.CharField('graus',default='sim', max_length=10)
    check_betw = models.CharField('betweenness',default='sim', max_length=10)
    check_eigen = models.CharField('eigenvector',default='sim', max_length=10)
    faixa_histo = models.FloatField('Faixa',default=0.2)
    exc_cluster = models.IntegerField('Exclusao_de_cluster')
    radio_r = models.FloatField('Representatividade_minima', default=0.0)
    nc =  models.IntegerField('CLusters dos temas principais', default=1)

class CorrigePalavra(models.Model):
    palavra_correta = models.TextField('palavra_correta')
    palavra = models.TextField('palavra')

    def __str__(self):
        return self.palavra


class Subtemas(models.Model):
    temas = models.TextField('Temas')
    subtemas = models.TextField('Subtemas')

    def __str__(self):
        return self.temas


class Clusters(models.Model):
    etapa = models.IntegerField('Etapa', null=True)
    nucleos = models.TextField('Nucleos')
    q_nucleos = models.IntegerField('Qtdd de Núcleos', null=True)
    subtemas = models.TextField('Subtemas')
    q_subtemas = models.IntegerField('Qtdd de subtemas', null=True)
    situacao = models.TextField('Situação')

    def __str__(self):
        return self.nucleos

class MapasTemasESubtemas(models.Model):
    tema = models.TextField('Tema')
    subtema = models.TextField('Subtema')
    irt_l = models.FloatField('IRT (subtema) Local Referênciado')
    
    def __str__(self):
        return self.tema