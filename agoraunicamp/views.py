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
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,render_to_response,redirect
from django.core.urlresolvers import reverse
from taggit.models import Tag
from .forms import DocumentForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from itertools import chain



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
    u = User.objects.get(user=self.request.user) 
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    context['projetos'] = Projeto.objects.all()

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
    #print user
    
    #busca o projeto do usuario
    projeto_atual = user.projeto
    #print projeto_atual
    
    #busca a etapa do projeto
    projeto_obj = Projeto.objects.get(sigla__exact=projeto_atual)
    etapa_atual = projeto_obj.etapa_prj
    #print etapa_atual

    #buscando as publicacoes validas
    publicacoes = Publicacao.objects.filter(projeto__sigla=projeto_atual, published='sim', etapa_publ=etapa_atual).order_by('-publ_date')
        
    #1. Questoes
    #busca as questões que o usuário já respondeu e define as nao respondidads    
    questions = Question.objects.filter(projeto__sigla=projeto_atual, published='sim', etapa_publ=etapa_atual).order_by('-publ_date')
    answered = Answer.objects.filter(user=user)
    answered_questions = [a.question for a in answered]
    questions_not_answered = list(set(questions) - set(answered_questions))

    #2. Artigos
    artigos = Article.objects.filter(projeto__sigla=projeto_atual, published='sim', etapa_publ=etapa_atual).order_by('-publ_date')

    #3. Relatorios
    relatorios = Relatorio.objects.filter(projeto__sigla=projeto_atual, published='sim', etapa_publ=etapa_atual).order_by('-publ_date')

    #4. Debates
    debates = Topic.objects.filter(projeto__sigla=projeto_atual, published='sim', etapa_publ=etapa_atual).order_by('-publ_date')
    
    #seleciona a etaoa corrente do projeto
    etapas = []
    for idx in range(1,6):
        if int(projeto_obj.etapa_prj) == idx:
            etapas.append("actual")
        if int(projeto_obj.etapa_prj) > idx:            
            etapas.append("past")        
        if int(projeto_obj.etapa_prj) < idx:          
            etapas.append("future")

    context['artigos'] = artigos
    context['questoes'] = questions_not_answered
    context['relatorios'] = relatorios    
    context['projeto'] = projeto_obj.projeto
    context['sigla'] = user.projeto
    context['debates'] = debates
    context['topic_user'] = User.objects.get(user=self.request.user)
    context['topic_users'] = TopicAnswer.objects.all()      
    context['etapas'] = etapas
    context['etapas_txt'] = get_object_or_404(projeto_obj.etapa_set , etapa=projeto_obj.etapa_prj)
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
        return redirect(request.META['HTTP_REFERER'])
    if success == True:
        messages.success(request, "Inclusão de apelido com sucesso")
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, error_message)
        return redirect(request.META['HTTP_REFERER'])

def agoraconfiguracaoemail(request):
    user = User.objects.get(user=request.user)    
    email = request.POST['text-email']
    if email:        
        user.email = email
        user.save()
        success = True
    else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
        return redirect(request.META['HTTP_REFERER'])
    if success == True:
        messages.success(request, "Inclusão de email com sucesso")
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, error_message)
        return redirect(request.META['HTTP_REFERER'])

def agoraconfiguracaoapelidoremove(request):
    user = User.objects.get(user=request.user)   
    user.nickname = user.primeiro_nome
    user.save()
    success = True
    if success == True:
        messages.success(request, "Apelido excluido com sucesso")
        return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, error_message)
        return redirect(request.META['HTTP_REFERER'])

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

        if form.is_valid():
            if request.FILES['arquivo'].name.endswith('.pdf'):
                x = MeuEspaco(user=nome, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Artigo', arquivo= request.FILES['arquivo'], projeto=projeto)
                x.save()
                success = True
                if success == True:
                    messages.success(request, "Arquivo enviado com sucesso")
                    return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, "Arquivo não enviado. Apenas arquivos PDF são aceitos.")
                return redirect(request.META['HTTP_REFERER'])
        
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
        us = User.objects.get(user=request.user)
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


def tag_search(request, tag_name):
  answered_questions_tag = []
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  questions = Question.objects.filter(exp_date__gt=timezone.now())
  answered = Answer.objects.filter(user=user)
  answered_questions = [a.question for a in answered]
  auth_user = request.user
  topics = Topic.objects.filter(projeto__sigla=user.projeto, tags__name__in=[tag_name]).order_by('-publ_date')
  questions_tag = Question.objects.filter(tags__name__in=[tag_name],projeto__sigla=user.projeto).distinct()
  article = Article.objects.filter(publ_date__lte=timezone.now(),projeto__sigla=user.projeto,tags__name__in=[tag_name]).order_by('-publ_date').distinct()
  relatorio = Relatorio.objects.filter(publ_date__lte=timezone.now(),projeto__sigla=user.projeto,tags__name__in=[tag_name]).order_by('-publ_date').distinct()
  not_answered = list(set(questions) - set(answered_questions))
  not_answered_tag = list(set(questions_tag) - set(answered_questions))
  projeto_nome = Projeto.objects.filter(sigla=user.projeto).first()
  result_list = sorted(
        chain(relatorio, article, not_answered_tag, topics),
        key=lambda instance: instance.publ_date, reverse=True)
  return render(request, 'agoraunicamp/agora-search.html',
    { 'article' : Article.objects.filter(publ_date__lte=timezone.now(),projeto__sigla=user.projeto).order_by('-publ_date'),
      'relatorio': Relatorio.objects.filter(publ_date__lte=timezone.now(),projeto__sigla=user.projeto).order_by('-publ_date'),
      'question' : Question.objects.filter(projeto__sigla=user.projeto),
      'not_answered': not_answered,
      'not_answered_tag': answered_questions_tag,
      'timeline': result_list,
      'tag' : tag_name,
      'topic_user' : User.objects.get(user=auth_user),
      'topic_users' : TopicAnswer.objects.all(),
      'projeto' : projeto_nome.projeto,
      'sigla' : user.projeto,

    })

def atualizaProjeto(request, projeto_nome):
    User.objects.filter(user=request.user).update(projeto=projeto_nome)
    return redirect('agoraunicamp:paginainicial')

def save_topic_answer_home(request, topic_id):
  topic = get_object_or_404(Topic, pk=topic_id)
  auth_user = AuthUser.objects.get(username=request.user)
  topic_user = User.objects.get(user=auth_user)
  answered_topic = TopicAnswer.objects.filter(user=topic_user, topic=topic).count()
  if answered_topic:
    error_message = 'Você já respondeu este tópico.'
    messages.error(request, error_message)
  else:
    answer = request.POST['text']
    if answer:
      answer_model = TopicAnswer(user=topic_user, topic=topic, text=answer)
      answer_model.save()
    else:
      messages.error(request, "Parece que você deixou o campo em branco. Por favor, tente novamente.")
    return redirect(request.META['HTTP_REFERER']+"#area%s"%(topic_id))

def save_topic_answer_home_edit(request, topic_id):
  topic = get_object_or_404(Topic, pk=topic_id)
  auth_user = AuthUser.objects.get(username=request.user)
  topic_user = User.objects.get(user=auth_user)
  answered_topic = TopicAnswer.objects.filter(user=topic_user, topic=topic).delete()
  answer = request.POST['text']
  if answer:
      answer_model = TopicAnswer(user=topic_user, topic=topic, text=answer)
      answer_model.save()
  else:
      messages.error(request, "Parece que você deixou o campo em branco. Por favor, tente novamente.")

  return redirect(request.META['HTTP_REFERER'] + "#area%s"%(topic_id))
  
def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type
  success = False
  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
    error_message = 'Você já votou nesta questão.'
    messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:participe'))
  try:
    # Save the answer
    if question_type == '1':
      answer = question.choice_set.get(pk=request.POST['choice'])
      if answer:
        answer_model = Answer(user=user, question=question, choice=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '2':
      answer = request.POST.getlist('choice')
      if answer:
        for choice_id in answer:
          choice = question.choice_set.get(pk=choice_id)
          answer_model = Answer(user=user, question=question, choice=choice)
          answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '3':
      answer = request.POST['text']
      if answer:
        answer_model = Answer(user=user, question=question, text=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
    if success == True:
      messages.success(request, "Obrigado por participar!")
    else:
      messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:participe'))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return HttpResponseRedirect(reverse('agora:participe'))


def vote_initial(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type
  success = False
  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
    error_message = 'Você já votou nesta questão.'
    messages.error(request, error_message)
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
  try:
    # Save the answer
    if question_type == '1':
      answer = question.choice_set.get(pk=request.POST['choice'])
      if answer:
        answer_model = Answer(user=user, question=question, choice=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '2':
      answer = request.POST.getlist('choice')
      if answer:
        for choice_id in answer:
          choice = question.choice_set.get(pk=choice_id)
          answer_model = Answer(user=user, question=question, choice=choice)
          answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '3':
      answer = request.POST['text']
      if answer:
        answer_model = Answer(user=user, question=question, text=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
    if success == True:
      messages.success(request, "Obrigado por participar!")
    else:
      messages.error(request, error_message)
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))

def vote_timeline(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type
  success = False
  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
    error_message = 'Você já votou nesta questão.'
    messages.error(request, error_message)
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
  try:
    # Save the answer
    if question_type == '1':
      answer = question.choice_set.get(pk=request.POST['choice'])
      if answer:
        answer_model = Answer(user=user, question=question, choice=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '2':
      answer = request.POST.getlist('choice')
      if answer:
        for choice_id in answer:
          choice = question.choice_set.get(pk=choice_id)
          answer_model = Answer(user=user, question=question, choice=choice)
          answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '3':
      answer = request.POST['text']
      if answer:
        answer_model = Answer(user=user, question=question, text=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
    if success == True:
      messages.success(request, "Obrigado por participar!")
    else:
      messages.error(request, error_message)
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
