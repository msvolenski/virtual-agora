# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render,render_to_response,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.contrib.auth.models import User as AuthUser
from agora.models import Choice, Question, InitialListQuestion
from .decorators import term_required
from django.views import generic
from .models import Termo, User, Answer, MeuEspaco, Message, Projeto
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,render_to_response,redirect
from django.core.urlresolvers import reverse
from taggit.models import Tag
from .forms import DocumentForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from conheca.models import Article
from resultados.models import Relatorio
from itertools import chain
from agora.models import Choice, Question, InitialListQuestion


@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class MuralView(generic.ListView):
  template_name = 'agoraunicamp/agora-mural.html'

  def get_context_data(self, **kwargs):
    context = super(MuralView, self).get_context_data(**kwargs)
    user = User.objects.get(user=self.request.user)
    questions = Question.objects.filter(exp_date__gt=timezone.now())
    answered = Answer.objects.filter(user=user)
    answered_questions = [a.question for a in answered]
    not_answered = list(set(questions) - set(answered_questions))
    try:
        initial = InitialListQuestion.objects.filter(select=1,projeto=user.projeto).first() #pega a lista
        initial_list = [c.name for c in initial.questions.all()]
    except:
        initial_list=[0]
    not_answered_list=[str(f.id) for f in not_answered]
    initial_list_user = list(set(initial_list).intersection(not_answered_list))
    if not initial_list_user:
        first_question = 'none'
    else:
        first_question = initial_list_user[0]
    projeto_nome = Projeto.objects.filter(sigla=user.projeto).first()
    context['initial_list'] = initial_list
    context['not_answered_list'] = not_answered_list
    context['initial_list_user'] = initial_list_user
    context['first_question'] = first_question
    context['question'] = Question.objects.all()
    context['not_answered'] = list(set(questions) - set(answered_questions))
    context['not_answered'].reverse()
    context['message_participe'] =  Message.objects.filter(published='Sim',kind='4',projeto=user.projeto).order_by('-publ_date')
    context['message_conheca'] =  Message.objects.filter(published='Sim',kind='1',projeto=user.projeto).order_by('-publ_date')
    context['message_resultados'] =  Message.objects.filter(published='Sim',kind='2',projeto=user.projeto).order_by('-publ_date')
    context['message_comunidade'] =  Message.objects.filter(published='Sim',kind='3',projeto=user.projeto).order_by('-publ_date')
    context['nickname'] = user.nickname
    context['projeto'] = projeto_nome.projeto
    context['sigla'] = user.projeto
    return context


  def get_queryset(self):
    return Question.objects.all()



@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class MeuEspacoOutrosView(generic.ListView):
  template_name = 'agoraunicamp/meu-espaco-outros.html'

  def get_context_data(self, **kwargs):
    context = super(MeuEspacoOutrosView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    tags = Tag.objects.all().distinct()
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
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    context['tags'] = tags
    context['form'] = DocumentForm
    return context

  def get_queryset(self):
    return

@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class MeuEspacoDebateView(generic.ListView):
  template_name = 'agoraunicamp/meu-espaco-debate.html'

  def get_context_data(self, **kwargs):
    context = super(MeuEspacoDebateView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    tags = Tag.objects.all().distinct()
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

  def get_queryset(self):
    return

  def get_context_data(self, **kwargs):
    context = super(AgoraView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    context['projetos'] = Projeto.objects.all()
    return context

@method_decorator(login_required(login_url='agora:login'), name='dispatch')
class TermoView(generic.ListView):
  template_name = 'agoraunicamp/termo.html'

  def get_queryset(self):
    return


#PROJETO
@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class PaginaInicialView(generic.ListView):
  """PDPU home with it's subpages"""
  template_name = 'agoraunicamp/agora-pagina-inicial.html'

  def get_queryset(self):
    return

  def get_context_data(self, **kwargs):
    context = super(PaginaInicialView, self).get_context_data(**kwargs)
    user = User.objects.get(user=self.request.user)
    questions = Question.objects.filter(projeto=user.projeto, exp_date__gt=timezone.now(),question_status='p')
    answered = Answer.objects.filter(user=user)
    answered_questions = [a.question for a in answered]
    article = Article.objects.filter(projeto=user.projeto, publ_date__lte=timezone.now()).order_by('-publ_date')
    relatorio = Relatorio.objects.filter(projeto=user.projeto, publ_date__lte=timezone.now()).order_by('-publ_date')
    not_answered = list(set(questions) - set(answered_questions))
    result_list = sorted(
        chain(relatorio, article, not_answered),
        key=lambda instance: instance.publ_date, reverse=True)

    projeto_nome = Projeto.objects.filter(sigla=user.projeto).first()

    context['article'] = Article.objects.filter(publ_date__lte=timezone.now(), projeto=user.projeto).order_by('-publ_date')
    context['relatorio'] = Relatorio.objects.filter(publ_date__lte=timezone.now(),projeto=user.projeto).order_by('-publ_date')
    context['question'] = Question.objects.filter(projeto=user.projeto)
    context['not_answered'] = list(set(questions) - set(answered_questions))
    context['not_answered'].reverse()
    context['timeline'] = result_list
    context['nickname'] = user.nickname

    context['projeto'] = projeto_nome.projeto
    context['sigla'] = user.projeto
    return context


def agoraconfiguracaoapelido(request):
    username = AuthUser.objects.get(username=request.user)
    user = username.user
    apelido = request.POST['text-apelido']
    if apelido:
        apelido_user = User.objects.get(user=user)
        apelido_user.nickname = apelido
        apelido_user.save()
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
    us = User.objects.get(user=request.user)
    user = us.user
    email = request.POST['text-email']
    if email:
        email_user = User.objects.get(user=user)
        email_user.email = email
        email_user.save()
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
    us = User.objects.get(user=request.user)
    user = us.user
    apelido_user = User.objects.get(user=user)
    apelido_user.nickname = user.user.primeiro_nome
    apelido_user.save()

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
    return HttpResponseRedirect(reverse('agora:home'))

def term_not_accepted(request):
    return HttpResponseRedirect(reverse('agoraunicamp:login'))



def enviaDadosMeuEspaco(request):
    us = User.objects.get(user=request.user)
    user = us.user
    if request.method == 'POST':
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
                x = MeuEspaco(user=user.username, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Artigo', arquivo= request.FILES['arquivo'])
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
            x = MeuEspaco(user=user.username, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Artigo')
            x.save()
            messages.success(request, "Link enviado com sucesso")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, "Você não enviou nenhum artigo. Caso queira enviar apenas um comentário vá em outras sugestões")
            return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])


def enviaDadosMeuEspacoDebate(request):
        us = User.objects.get(user=request.user)
        user = us.user
        if request.method == 'POST':
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
            x = MeuEspaco(user=user.username, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Debate')
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
        user = us.user
        if request.method == 'POST':
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
            x = MeuEspaco(user=user.username, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Questão')
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
    us = User.objects.get(user=request.user)
    user = us.user
    if request.method == 'POST':
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
                x = MeuEspaco(user=user.username, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Outros', arquivo= request.FILES['arquivo'])
                x.save()
                success = True
                if success == True:
                    messages.success(request, "Dados enviados com sucesso.")
                    return redirect(request.META['HTTP_REFERER'])

        else:
            x = MeuEspacoArtigo(user=user.username, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Outros')
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
  questions_tag = Question.objects.filter(tags__name__in=[tag_name],projeto=user.projeto).distinct()
  article = Article.objects.filter(publ_date__lte=timezone.now(),projeto=user.projeto,tags__name__in=[tag_name]).order_by('-publ_date').distinct()
  relatorio = Relatorio.objects.filter(publ_date__lte=timezone.now(),projeto=user.projeto,tags__name__in=[tag_name]).order_by('-publ_date').distinct()
  not_answered = list(set(questions) - set(answered_questions))
  not_answered_tag = list(set(questions_tag) - set(answered_questions))
  result_list = sorted(
        chain(relatorio, article, not_answered_tag),
        key=lambda instance: instance.publ_date, reverse=True)
  return render(request, 'agoraunicamp/agora-search.html',
    { 'article' : Article.objects.filter(publ_date__lte=timezone.now(),projeto=user.projeto).order_by('-publ_date'),
      'relatorio': Relatorio.objects.filter(publ_date__lte=timezone.now(),projeto=user.projeto).order_by('-publ_date'),
      'question' : Question.objects.filter(projeto=user.projeto),
      'not_answered': not_answered,
      'not_answered_tag': answered_questions_tag,
      'timeline': result_list,
      'tag' : tag_name,

    })

def atualizaProjeto(request, projeto_nome):
    #us = User.objects.get(user=request.user)
    #user = us.user
    #user.set(projeto=projeto_nome)
    User.objects.filter(user=request.user).update(projeto=projeto_nome)
    return redirect('agoraunicamp:mural')
