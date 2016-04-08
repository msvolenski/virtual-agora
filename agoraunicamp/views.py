# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render,render_to_response,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.contrib.auth.models import User as AuthUser
from agora.models import Choice, Question, InitialListQuestion, Message
from .decorators import term_required
from django.views import generic
from .models import Termo, User, Answer, MeuEspaco
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,render_to_response,redirect
from django.core.urlresolvers import reverse
from taggit.models import Tag
from .forms import DocumentForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


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
  template_name = 'agoraunicamp/agora-inicial.html'

  def get_queryset(self):
    return

  def get_context_data(self, **kwargs):
    context = super(AgoraView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    return context

@method_decorator(login_required(login_url='agora:login'), name='dispatch')
class TermoView(generic.ListView):
  template_name = 'agoraunicamp/termo.html'

  def get_queryset(self):
    return






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
