from .models import Choice, Question, Answer, User
# from conheca.models import Topic
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from taggit.models import Tag


#============================================================================
# @method_decorator(login_required(login_url='/agora/login/')
# DEVE SER COLOCADO EM TODAS AS VIEWS NÃO PÚBLICAS!
#============================================================================

@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class HomeView(generic.ListView):
  template_name = 'agora/home.html'

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:2]

#============================================================================
# VIEW DA PÁGINA PRINCIPAL DO PLANO DIRETOR PARTICIPATIVO DA UNICAMP
# Basicamente atualiza as timelines das quatros partes: Conheça, Participe, Resultados e Comunidade
#============================================================================
@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class PdpuView(generic.ListView):

  template_name = 'agora/pagina-pdpu.html'
  # model = Topic

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

  #context_object_name = 'Question_list'
  #Configura quantos links serQo mostrados na ordem da data de publicação

  #Contém os outros objetos além de "AdicionaLink": Question, ...
  # def get_context_data(self, **kwargs):
    # context = super(PdpuView, self).get_context_data(**kwargs)
    # context['Question'] = Question.objects.filter( #Label 'Question" deve ser usada no template
    #   pub_date__lte=timezone.now()
    # ).order_by('-pub_date')[:4]
    # context['tag'] = Tag.objects.all()
    # context['user_nome'] = self.request.user
    # context['q'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
    #número que define quantas "Questions" vão aparecer
    # return context

#=========================================================================
# A classe abaixo cria a "timeline" de questões na Página PDPU - PARTICIPE
#=========================================================================
@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class PdpuParticipeView(generic.ListView):
  template_name = 'agora/pdpu-participe.html'
  model = Question

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

  def get_context_data(self, **kwargs):
    context = super(PdpuParticipeView, self).get_context_data(**kwargs)

    user = User.objects.get(user=self.request.user)
    questions = Question.objects.filter(exp_date__gt=timezone.now())
    answered =  Answer.objects.filter(user_id=user.id)
    answered_questions = [a.question for a in answered]

    context['not_answered'] = list(set(questions) - set(answered_questions))
    return context

@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class PdpuResultadosView(generic.ListView):
  template_name = 'agora/pdpu-resultados.html'
  model = Question

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

  # def get_context_data(self, **kwargs):
  #   context = super(PdpuResultadosView, self).get_context_data(**kwargs)
  #   context['user_nome'] = self.request.user
  #   context['q'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
  #   return context

@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class PdpuComunidadeView(generic.ListView):
  template_name = 'agora/pdpu-comunidade.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class DetailView(generic.DetailView):
  model = Question
  template_name = 'agora/detail.html'

  def get_queryset(self):
    """Excludes any questions that aren't published yet."""
    return Question.objects.filter(pub_date__lte=timezone.now())

@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class ResultsView(generic.DetailView):
  model = Question
  template_name = 'agora/result.html'

  def get_queryset(self):
    """Excludes any questions that aren't published yet."""
    return Question.objects.all()

  def get_context_data(self, **kwargs):
    context = super(ResultsView, self).get_context_data(**kwargs)
    context['user'] = User.objects.all()
    context['answered'] = Answer.objects.all()
    # context['votodousuario'] = VotoDoUsuario.objects.all()

    return context


def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type

  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
    return HttpResponseRedirect(reverse('agora:posvotacao'))

  try:
    # Save the answer
    if question_type == 'o':
      answer = question.choice_set.get(pk=request.POST['choice'])
      answer_model = Answer(user=user, question=question, choice=answer)
      answer_model.save()
    elif question_type == 'm':
      answer = request.POST.getlist('choice')
      for choice_id in answer:
        choice = question.choice_set.get(pk=choice_id)
        answer_model = Answer(user=user, question=question, choice=choice)
        answer_model.save()
    elif question_type == 't':
      answer = request.POST['text']
      answer_model = Answer(user=user, question=question, text=answer)
      answer_model.save()
    return HttpResponseRedirect(reverse('agora:posvotacao'))
  except (KeyError, Choice.DoesNotExist):
    # Redisplay the question voting form.
    return render(request, 'agora/detail.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    })

def posvotacao(request):
  return render(request, 'agora/pos-votacao.html')
