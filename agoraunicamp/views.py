# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render,render_to_response,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.contrib.auth.models import User as AuthUser
from .decorators import term_required
from django.views import generic
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render,render_to_response,redirect
from django.core.urlresolvers import reverse
from taggit.models import Tag
from .forms import DocumentForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from itertools import chain
from collections import *
import codecs
import os



@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class MeuEspacoOutrosView(generic.ListView):
  template_name = 'agoraunicamp/meu-espaco-outros.html'

  def get_context_data(self, **kwargs):
    context = super(MeuEspacoOutrosView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    tags = Tag.objects.all().distinct()
    projetos = Projeto.objects.all().distinct()
    context['projetos'] = projetos
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    context['tags'] = tags
    context['form'] = DocumentForm
    return context

  def get_queryset(self):
    return

@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class MeuEspacoQuestaoView(generic.ListView):
  template_name = 'agoraunicamp/meu-espaco-questao.html'

  def get_context_data(self, **kwargs):
    context = super(MeuEspacoQuestaoView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    tags = Tag.objects.all().distinct()
    projetos = Projeto.objects.all().distinct()
    context['projetos'] = projetos
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    context['tags'] = tags
    context['form'] = DocumentForm
    return context

  def get_queryset(self):
    return

@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class MeuEspacoArtigoView(generic.ListView):
  template_name = 'agoraunicamp/meu-espaco-artigo.html'

  def get_context_data(self, **kwargs):
    context = super(MeuEspacoArtigoView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    tags = Tag.objects.all().distinct()
    projetos = Projeto.objects.all().distinct()
    context['projetos'] = projetos
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    context['tags'] = tags
    context['form'] = DocumentForm
    return context

  def get_queryset(self):
    return

@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class MeuEspacoDebateView(generic.ListView):
  template_name = 'agoraunicamp/meu-espaco-debate.html'

  def get_context_data(self, **kwargs):
    context = super(MeuEspacoDebateView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    tags = Tag.objects.all().distinct()
    projetos = Projeto.objects.all().distinct()
    context['projetos'] = projetos
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    context['tags'] = tags
    context['form'] = DocumentForm
    return context

  def get_queryset(self):
    return


@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class AgoraConfiguracaoView(generic.ListView):
  template_name = 'agoraunicamp/agora-configuracoes.html'

  def get_context_data(self, **kwargs):
    context = super(AgoraConfiguracaoView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    return context

  def get_queryset(self):
    return


@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class AgoraView(generic.ListView):
  template_name = 'agoraunicamp/agora-projetos.html'
  #usua = User.objects.all()
  #for i in usua:
  #    print i.nickname
  def get_queryset(self):
    return

  def get_context_data(self, **kwargs):
    context = super(AgoraView, self).get_context_data(**kwargs)
    user = User.objects.get(user=self.request.user) 
    autent = self.request.user.is_authenticated
    
    context['user'] = User.objects.get(user=self.request.user) 
    context['projetos'] = Projeto.objects.all()
    context['autenticado'] = autent

    return context

@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
class TermoView(generic.ListView):
  template_name = 'agoraunicamp/termo.html'

  def get_queryset(self):
    return


#PROJETO
@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class PaginaInicialView(generic.ListView):
  #"""PDPU home with it's subpages"""
  template_name = 'agoraunicamp/agora-pagina-inicial.html'

  def get_queryset(self):
    return

  def get_context_data(self, **kwargs):    
    context = super(PaginaInicialView, self).get_context_data(**kwargs)
    
    #busca usuário
    user = User.objects.get(user=self.request.user)
    answered = Answer.objects.filter(user=user)

    autent = self.request.user.is_authenticated
        
    #busca o projeto do usuario
    projeto_atual = user.projeto
    #print projeto_atual
    
    #busca a etapa do projeto
    user.projeto = user.projeto
    etapa_atual = user.projeto.etapa_prj
    #print etapa_atual

    #buscando as publicacoes validas
    publicacoes = Publicacao.objects.filter(projeto=user.projeto, published='sim', etapa_publ=etapa_atual).order_by('-publ_date')
        
    #1. Questoe
    #busca as questões que o usuário já respondeu e define as nao respondidads    
    questions = Question.objects.filter(projeto=projeto_atual, published='sim', etapa_publ=etapa_atual).order_by('-publ_date')
    answered = Answer.objects.filter(user=user)
    answered_questions = [a.question for a in answered]
    questions_not_answered = list(set(questions) - set(answered_questions))


    
    
    
    
    #2. Artigos
    artigos = Article.objects.filter(projeto=user.projeto, published='sim', etapa_publ=etapa_atual).order_by('-publ_date')

    #3. Relatorios - gera resultados
    relatorios = Relatorio.objects.filter(projeto=user.projeto, published='sim', etapa_publ=etapa_atual).order_by('-publ_date')
    if relatorios:
        for objeto in relatorios:
            if objeto.tipo == '2':
                gera_resultados(objeto)

   
    #3.1 Relatórios - prepara propostas de questoes
    relatorios_prop_do_usuario = Relatorio.objects.filter(projeto=user.projeto, published='sim', etapa_publ=etapa_atual, propostas_org='1').order_by('-publ_date')
    
    for rel in relatorios_prop_do_usuario:
        questao_associada = rel.questao
        propostas = Answer.objects.filter(question=questao_associada)
        for prop in propostas:
            obj, created = Proposta.objects.get_or_create(relatorio=rel,proposta_text=prop)   
   
    #4. Debates
    debates = Topic.objects.filter(projeto=user.projeto, published='sim', etapa_publ=etapa_atual).order_by('-publ_date')
    #for d in debates:
    #  print d.all()
    #seleciona a etaoa corrente do projeto
    etapas = []
    id_hist = []
    for idx in range(1,6):
        if int(user.projeto.etapa_prj) == idx:
            etapas.append("actual")            
        if int(user.projeto.etapa_prj) > idx:            
            etapas.append("past")
            id_hist.append('etapa_hist_' + str(idx))       
        if int(user.projeto.etapa_prj) < idx:          
            etapas.append("future")

    context['artigos'] = artigos
    context['questoes'] = questions_not_answered
    context['relatorios'] = relatorios    
    context['projeto'] = user.projeto.projeto
    context['sigla'] = user.projeto.sigla
    context['debates'] = debates
    context['id_hist'] = id_hist
    context['autenticado'] = autent
    context['topic_user'] = User.objects.get(user=self.request.user)
    context['topic_users'] = TopicAnswer.objects.all()      
    context['user'] = User.objects.get(user=self.request.user)
    context['etapas'] = etapas
    context['etapas_txt'] = get_object_or_404(user.projeto.etapa_set , etapa=user.projeto.etapa_prj)
    return context


def agoraconfiguracaoapelido(request):
    user = User.objects.get(user=request.user)    
    apelido = request.POST['text-apelido']
    if apelido:
        user.nickname = apelido
        user.save()
        success = True
    else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
        return HttpResponse('error_message')
    if success == True:
        messages.success(request, "Inclusão de apelido com sucesso")
        return HttpResponse('success')
    else:
        messages.error(request, error_message)
        return HttpResponse('error_message')

def agoraconfiguracaoemail(request):
    user = User.objects.get(user=request.user)    
    email = request.POST['text-email']       
    try:
        validate_email(email)
        valid_email = True
    except ValidationError:
        valid_email = False
    
    if valid_email == True:                

        user.email = email
        user.save()
    else:
        user.email = "Email inválido. Insira novamente"
        user.save()
    return HttpResponse('success')


def agoraconfiguracaoapelidoremove(request):
    user = User.objects.get(user=request.user)   
    user.nickname = user.primeiro_nome
    user.save()         
    return HttpResponse('success')

def term_accepted(request):
    username = AuthUser.objects.get(username=request.user)
    user = username.user
    cond = Termo.objects.get(user=user)
    cond.delete()
    cond1 = Termo(user=user,condition='Sim')
    cond1.save()
    return HttpResponseRedirect(reverse('agoraunicamp:agora'))

def term_not_accepted(request):
    return HttpResponseRedirect(reverse('agoraunicamp:login'))

def enviaDadosMeuEspaco(request):    
    user = User.objects.get(user=request.user)   
    nome = user.primeiro_nome + ' ' + user.ultimo_nome
    if request.method == 'POST':
        projeto = request.POST['categoriaproj']
        categoria = request.POST['categoriatag']
        comentario = request.POST['comentario']
        link = request.POST['link']
        if link != '':
            validate = URLValidator()
            try:
                validate(link)
            except:
                messages.error(request, "URL incorreta. Envie novamente.")
                return redirect(request.META['HTTP_REFERER'])
        form = DocumentForm(request.POST, request.FILES)
        
        try:
            request.FILES['arquivo']
            test = 'success'
        except:
            test  ='fail'
        if test == 'success':
            if form.is_valid():
                if request.FILES['arquivo'].name.endswith('.pdf'):
                    x = MeuEspaco(user=nome, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Artigo', arquivo=request.FILES['arquivo'], projeto=projeto)
                    x.save()
                    success = True
                    if success == True:
                        messages.success(request, "Arquivo enviado com sucesso")
                        return redirect(request.META['HTTP_REFERER'])
                else:
                    messages.error(request, "Arquivo não enviado. Apenas arquivos PDF são aceitos.")
                    return redirect(request.META['HTTP_REFERER'])
        else:
            x = MeuEspaco(user=nome, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Artigo', projeto=projeto)

        
        if link !='':
            form = DocumentForm() #A empty, unbound form
            x = MeuEspaco(user=nome, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Artigo',projeto=projeto)
            x.save()
            messages.success(request, "Link enviado com sucesso")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, "Você não enviou nenhum artigo. Caso queira enviar apenas um comentário vá em outras sugestões")
            return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])


def enviaDadosMeuEspacoDebate(request):
        user = User.objects.get(user=request.user)
        nome = user.primeiro_nome + ' ' + user.ultimo_nome
        if request.method == 'POST':
            projeto = request.POST['categoriaproj']
            categoria = request.POST['categoriatag']
            comentario = request.POST['comentario']
            link = request.POST['link']
            if link != '':
                validate = URLValidator()
                try:
                    validate(link)
                except:
                    messages.error(request, "URL incorreta. Envie novamente.")
                    return redirect(request.META['HTTP_REFERER'])
            x = MeuEspaco(user=nome, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Debate', projeto=projeto)
            x.save()
            success = True
            if success == True and comentario !='' or link !='':
                messages.success(request, "Dados enviados com sucesso")
                return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, "Nenhum dado foi enviado")
                return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect(request.META['HTTP_REFERER'])

def enviaDadosMeuEspacoQuestao(request):
        user = User.objects.get(user=request.user)
        nome = user.primeiro_nome + ' ' + user.ultimo_nome
        if request.method == 'POST':
            projeto = request.POST['categoriaproj']
            categoria = request.POST['categoriatag']
            comentario = request.POST['comentario']
            link = request.POST['link']
            if link != '':
                validate = URLValidator()
                try:
                    validate(link)
                except:
                    messages.error(request, "URL incorreta. Envie novamente.")
                    return redirect(request.META['HTTP_REFERER'])
            x = MeuEspaco(user=nome, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Questão',projeto=projeto)
            x.save()
            success = True
            if success == True and comentario !='' or link !='':
                messages.success(request, "Dados enviados com sucesso")
                return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, "Nenhum dado foi enviado")
                return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect(request.META['HTTP_REFERER'])

def enviaDadosMeuEspacoOutros(request):
    user = User.objects.get(user=request.user)
    nome = user.primeiro_nome + ' ' + user.ultimo_nome
    if request.method == 'POST':
        projeto = request.POST['categoriaproj']
        categoria = request.POST['categoriatag']
        comentario = request.POST['comentario']
        link = request.POST['link']
        if link != '':
            validate = URLValidator()
            try:
                validate(link)
            except:
                messages.error(request, "URL incorreta. Envie novamente.")
                return redirect(request.META['HTTP_REFERER'])
        form = DocumentForm(request.POST, request.FILES)
        try:
            request.FILES['arquivo']
            test = 'success'
        except:
            test  ='fail'
        if test == 'success':            
            if form.is_valid():
                if request.FILES['arquivo'].name.endswith('.pdf'):
                    x = MeuEspaco(user=nome, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Outros', arquivo= request.FILES['arquivo'], projeto=projeto)
                    x.save()
                    success = True
                    if success == True:
                        messages.success(request, "Dados enviados com sucesso.")
                        return redirect(request.META['HTTP_REFERER'])

        else:
            x = MeuEspaco(user=nome, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Outros', projeto=projeto)
            x.save()
            messages.success(request, "Dados enviados com sucesso.")
            return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])




def atualizaProjeto(request, projeto_nome):
    novo_projeto = Projeto.objects.get(projeto=projeto_nome)
    User.objects.filter(user=request.user).update(projeto=novo_projeto)    
    return redirect('agoraunicamp:paginainicial')
    

def save_topic_answer_home(request, topic_id):
  topic = get_object_or_404(Topic, pk=topic_id)
  user = User.objects.get(user=request.user) 
  answered_topic = TopicAnswer.objects.filter(user=user, topic=topic).count()
  if answered_topic:
      error = 'Tópico já comentado. Você pode editar seu comentário.'
      return render(request, 'agoraunicamp/debate/error.html', {
          'menssagem':error
      }) 
  else:
    answer = request.POST['text']
    if answer:
      answer_model = TopicAnswer(user=user, topic=topic, text=answer)
      answer_model.save()
      return render(request, 'agoraunicamp/debate/comment.html', {
          'user': user,
          'comment': answer_model,
          'debate':topic,
      })
    else:
      messages.error(request, "Parece que você deixou o campo em branco. Por favor, tente novamente.")


def save_reply_answer_home(request, comment_id):
  comentario = get_object_or_404(TopicAnswer, pk=comment_id)
  user = User.objects.get(user=request.user)
  
  #testa se o usuário já replicou
  comentario_respondido = TopicAnswerReply.objects.filter(user=user, comment=comentario).count()

  if comentario_respondido:
      c =  get_object_or_404(TopicAnswerReply, user=user, comment=comentario) 
      error = 'Comentário já respondondido. Você pode editar sua resposta.'
      return render(request, 'agoraunicamp/debate/error.html', {
          'menssagem':error
      }) 
     
  else:
      text = request.POST['text']
    
      reply = TopicAnswerReply(user=user, comment=comentario, text=text, answer_date=timezone.now())
      reply.save()
      return render(request, 'agoraunicamp/debate/reply.html', {
          'user':user,
          'reply': reply,
          'comment':comentario,
      })

def save_reply_answer_edit(request, reply_id):
  reply = get_object_or_404(TopicAnswerReply, pk=reply_id)
  user = User.objects.get(user=request.user) 
  new_reply = request.POST['text']
  if new_reply:
      reply.text = new_reply
      reply.answer_date = timezone.now()
      reply.save() 
      return render(request, 'agoraunicamp/debate/reply.html', {
          'user':user,
          'reply': reply,          
      })  
  else:
      return HttpResponseForbidden('User does not own this reply to delete it.')
     
def delete_reply(request, reply_id):
  reply = get_object_or_404(TopicAnswerReply, pk=reply_id)
  user = User.objects.get(user=request.user)  
  if user != reply.user:
    return HttpResponseForbidden('User does not own this reply to delete it.')
  else:
    reply.delete()
    return HttpResponse('Successfully deleted reply.')

def delete_comment(request, comment_id):
  comment = get_object_or_404(TopicAnswer, pk=comment_id)
  user = User.objects.get(user=request.user)  
  if user != comment.user:
    return HttpResponseForbidden('User does not own this comment to delete it.')
  else:
    comment.delete()
    return HttpResponse('Successfully deleted reply.')

def save_topic_answer_home_edit(request, topic_id):
  topic = get_object_or_404(Topic, pk=topic_id)
  user = User.objects.get(user=request.user)  
  answered_topic = TopicAnswer.objects.filter(user=user, topic=topic).delete()
  answer = request.POST['text']
  if answer:
      answer_model = TopicAnswer(user=user, topic=topic, text=answer)
      answer_model.save()    
      return render(request, 'agoraunicamp/debate/comment.html', {
          'user': user,
          'debate': topic,
          'comment':answer_model,
      })
  else:
      return HttpResponseForbidden('User does not own this comment to edit it.')


def vote_timeline(request, question_id):
  #carrega usuario
  user = User.objects.get(user=request.user)
  
  #carrega questao
  question = get_object_or_404(Question, pk=question_id)
  
  #registra resposta de One Choice
  if question.question_type == '1':    
    if request.method == 'POST':
      answer = question.choice_set.get(pk=request.POST['choice'])
      answer_model = Answer(user=user, question=question, choice=answer)
      answer_model.save() 
      return HttpResponse('Sucesso')    
    else:
      error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
      return HttpResponse('error_message')

  #registra resposta de multiple Choice
  if question.question_type == '2':    
    if request.method == 'POST':
      answeru = request.POST.getlist('choice')
      for c in answeru:
        choice = question.choice_set.get(pk=c)
        answer_model = Answer(user=user, question=question, choice=choice)
        answer_model.save() 
      return HttpResponse('Sucesso')    
    else:
      error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
      return HttpResponse('error_message')

  #registra resposta de text
  if question.question_type == '3':    
    answer = request.POST['text']
    if answer:
      answer_model = Answer(user=user, question=question, text=answer)
      answer_model.save()#       success = True     
      return HttpResponse('Sucesso')
    else:
      error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
      return HttpResponse('error_message')
  
  #registra resposta de multiple Choice
  if question.question_type == '4':    
    if request.method == 'POST':     
      
      for key, value in request.POST.items():            
        if 'proposal' in key and value:     
          answer_model = Answer(user=user, question=question, text=value)
          answer_model.save() 
      return HttpResponse('Sucesso')
    else:
      error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
      return HttpResponse('error_message')

def simple_upload(request):
    user = User.objects.get(user=request.user)

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        user.avatar = myfile
        user.save()
        return HttpResponse('Success')
    return redirect(request.META['HTTP_REFERER']+"#question%s")

def gera_resultados(objeto):
    #gera arquivo json
    arq_json = codecs.open("agoraunicamp/static/agoraunicamp/arquivos/json/resultados_" + str(objeto.questao.pk) + "_" + str(objeto.filtro_staff) + ".json", 'w', 'utf-8') 
    nome = "/static/agoraunicamp/arquivos/json/resultados_" + str(objeto.questao.pk) + "_" + str(objeto.filtro_staff) + ".json"
    objeto.arquivo = nome
    objeto.save()
    print objeto.questao.pk

##### Carrega ore relatorios OneCHoice e MultiplaEscolha ##########################################################
    if objeto.questao.question_type == '1' or objeto.questao.question_type == '2': 
        
        #carrega e inicializa as escolhas da questao
        choices = {}
        choices_objs = Choice.objects.filter(question = objeto.questao)
        for choice in choices_objs:
            choices[choice.choice_text] = 0

        #carrega os resultados
        if objeto.filtro_staff == '9':
            #sem filtro
            resultados = Answer.objects.filter(question=objeto.questao)        
        else:
            #com filtro
            resultados = Answer.objects.filter(question=objeto.questao).filter(user__staff = objeto.filtro_staff) 
                      
        #Computa resiltados
        for k,v in choices.iteritems():            
            for item in resultados:
                if k == item.choice.choice_text:                    
                    choices[k] = choices[k] + 1
                
      
        #total de votos
        total = 0
        for k,v in choices.iteritems():
            total = total + v
      
        
        #gera JSON\
        arq_json.write("[\n")
        for k, v in choices.iteritems():
         
            perc = float(float(v)/float(total))*100         
            arq_json.write("    {\"name\": \"" + k + "\", \"value\": " + str(perc)+ "},\n" )    
        arq_json.seek(-2, os.SEEK_END)
        arq_json.write("\n]")
       
        return

def curtir_proposta(request, proposta_pk, tipo):

    user = User.objects.get(user=request.user)
    prop = Proposta.objects.get(pk=proposta_pk)
    obj, created = Curtir.objects.get_or_create(user=user, proposta=prop)
    if created:
        if tipo == 'curtir':
            prop.curtidas = prop.curtidas + 1            
            prop.indice = 1000 + prop.curtidas - prop.naocurtidas
            prop.save()
        if tipo == 'naocurtir':
            prop.naocurtidas = prop.naocurtidas + 1
            prop.indice = 1000 + prop.curtidas - prop.naocurtidas
            prop.save()      
    return HttpResponse('Sucesso')

def mudaEtapa(request, etapa_nova):
    user = User.objects.get(user=request.user)
    etapa_do_projeto = user.projeto.etapa_prj
    autent = request.user.is_authenticated
    
    if etapa_nova > etapa_do_projeto:
                #seleciona a etaoa corrente do projeto
        etapas = []
        id_hist = []
        for idx in range(1,6):
            if int(user.projeto.etapa_prj) == idx:
                etapas.append("actual")            
            if int(user.projeto.etapa_prj) > idx:            
                etapas.append("past")
                id_hist.append('etapa_hist_' + str(idx))       
            if int(user.projeto.etapa_prj) < idx:          
                etapas.append("future")
                
        return render(request, 'agoraunicamp/agora-pagina-inicial.html', {
            'projeto': user.projeto.projeto,
            'future': 'sim',
            'user': user,
            'autenticado': autent,
            'nova_etapa': etapa_nova,
            'etapas': etapas,
            'etapas_txt': get_object_or_404(user.projeto.etapa_set, etapa=user.projeto.etapa_prj),
        })
        
    if etapa_nova == etapa_do_projeto:
        return HttpResponseRedirect("/agora/paginainicial/")
        
    if etapa_nova < etapa_do_projeto:
            #2. Artigos
        artigos = Article.objects.filter(projeto=user.projeto, published='sim', etapa_publ=etapa_nova).order_by('-publ_date')

        #3. Relatorios - gera resultados
        relatorios = Relatorio.objects.filter(projeto=user.projeto, published='sim', etapa_publ=etapa_nova).order_by('-publ_date')
        if relatorios:
            for objeto in relatorios:
                if objeto.tipo == '2':
                    gera_resultados(objeto)

        #3.1 Relatórios - prepara propostas de questoes
        relatorios_prop_do_usuario = Relatorio.objects.filter(projeto=user.projeto, published='sim', etapa_publ=etapa_nova, propostas_org='1').order_by('-publ_date')

        for rel in relatorios_prop_do_usuario:
            questao_associada = rel.questao
            propostas = Answer.objects.filter(question=questao_associada)
            for prop in propostas:
                obj, created = Proposta.objects.get_or_create(relatorio=rel,proposta_text=prop)   

        #4. Debates
        debates = Topic.objects.filter(projeto=user.projeto, published='sim', etapa_publ=etapa_nova).order_by('-publ_date')
    
        #seleciona a etaoa corrente do projeto
        etapas = []
        id_hist = []
        for idx in range(1,6):
            if int(user.projeto.etapa_prj) == idx:
                etapas.append("actual")            
            if int(user.projeto.etapa_prj) > idx:            
                etapas.append("past")
                id_hist.append('etapa_hist_' + str(idx))       
            if int(user.projeto.etapa_prj) < idx:          
                etapas.append("future")
        
        return render(request, 'agoraunicamp/agora-pagina-inicial.html', {
          'projeto': user.projeto.projeto,
          'artigos':artigos,
          'relatorios': relatorios, 
          'debates': debates,
          'etapas': etapas,
          'etapas_txt': get_object_or_404(user.projeto.etapa_set, etapa=user.projeto.etapa_prj),
          'nova_etapa': etapa_nova,
          'hist': 'hist',
          'user': user,
          'autenticado': autent,
        })

    

  # question_type = question.question_type
  # success = False
  # # Query over the voted questions
  # answered_question = Answer.objects.filter(user=user, question=question).count()
  # if answered_question:
  #   error_message = 'Você já votou nesta questão.'
  #   messages.error(request, error_message)
  #   return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
  # try:
  #   # Save the answer
  #   if question_type == '1':
  #     answer = question.choice_set.get(pk=request.POST['choice'])
  #     if answer:
  #       answer_model = Answer(user=user, question=question, choice=answer)
  #       answer_model.save()
  #       success = True
  #     else:
  #       error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
  #   elif question_type == '2':
  #     answer = request.POST.getlist('choice')
  #     if answer:
  #       for choice_id in answer:
  #         choice = question.choice_set.get(pk=choice_id)
  #         answer_model = Answer(user=user, question=question, choice=choice)
  #         answer_model.save()
  #       success = True
  #     else:
  #       error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
  #   elif question_type == '3':
  #     answer = request.POST['text']
  #     if answer:
  #       answer_model = Answer(user=user, question=question, text=answer)
  #       answer_model.save()
  #       success = True
  #     else:
  #       error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
  #   if success == True:
  #     messages.success(request, "Obrigado por participar!")
  #   else:
  #     messages.error(request, error_message)
  #   return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
  # except (KeyError, Choice.DoesNotExist):
  #   messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
  #   return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
