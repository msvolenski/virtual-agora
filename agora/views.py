from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as AuthUser
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from conheca.models import Article
from resultados.models import Relatorio
from taggit.models import Tag
from itertools import chain
from .models import Choice, Question, Answer, User, InitialListQuestion


@method_decorator(login_required(login_url='agora:login'), name='dispatch')
class HomeView(generic.ListView):
  """Homepage of the website"""

  template_name = 'agora/home.html'
  
  def get_context_data(self, **kwargs):
    context = super(HomeView, self).get_context_data(**kwargs)
    
    user = User.objects.get(user=self.request.user)      
    questions = Question.objects.filter(exp_date__gt=timezone.now())
    answered = Answer.objects.filter(user=user)
    answered_questions = [a.question for a in answered] 
    b = InitialListQuestion.objects.filter(select=1).first() 
    context['question'] = Question.objects.all() 
    context['not_answered'] = list(set(questions) - set(answered_questions))
    context['not_answered'].reverse()
    context['initial_questions'] = b
    return context
  
  def get_queryset(self):
    return Question.objects.all()


@method_decorator(login_required(login_url='agora:login'), name='dispatch')
class PdpuView(generic.ListView):
  """PDPU home with it's subpages"""
  template_name = 'agora/pagina-pdpu.html'
  
  def get_queryset(self):
    
    return

  def get_context_data(self, **kwargs):
    context = super(PdpuView, self).get_context_data(**kwargs)

    user = User.objects.get(user=self.request.user)      
    questions = Question.objects.filter(exp_date__gt=timezone.now())
    answered = Answer.objects.filter(user=user)
    answered_questions = [a.question for a in answered]
    article = Article.objects.filter(publ_date__lte=timezone.now()).order_by('-publ_date')
    relatorio = Relatorio.objects.filter(publ_date__lte=timezone.now()).order_by('-publ_date') 
    not_answered = list(set(questions) - set(answered_questions))    
    result_list = sorted(
        chain(relatorio, article, not_answered),
        key=lambda instance: instance.publ_date, reverse=True)
    context['article'] = Article.objects.filter(publ_date__lte=timezone.now()).order_by('-publ_date')
    context['relatorio'] = Relatorio.objects.filter(publ_date__lte=timezone.now()).order_by('-publ_date')     
    context['question'] = Question.objects.all() 
    context['not_answered'] = list(set(questions) - set(answered_questions))    
    context['not_answered'].reverse()
    context['timeline'] = result_list
   
    return context



@method_decorator(login_required(login_url='agora:login'), name='dispatch')
class PdpuParticipeView(generic.ListView):
  """View with questions' timeline presented to the users"""

  template_name = 'agora/pdpu-participe.html'
  model = Question

  def get_queryset(self):
    return Question.objects.filter(publ_date__lte=timezone.now()).order_by('-publ_date')

  def get_context_data(self, **kwargs):
    context = super(PdpuParticipeView, self).get_context_data(**kwargs)

    user = User.objects.get(user=self.request.user)
    questions = Question.objects.filter(exp_date__gt=timezone.now())

    answered = Answer.objects.filter(user=user)
    answered_questions = [a.question for a in answered]

    context['not_answered'] = list(set(questions) - set(answered_questions))
    context['not_answered'].reverse()
    return context




@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class DetailView(generic.DetailView):
  model = Question
  template_name = 'agora/detail.html'


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
    return HttpResponseRedirect(reverse('agora:pdpu-participe'))

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
    return HttpResponseRedirect(reverse('agora:pdpu-participe'))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return HttpResponseRedirect(reverse('agora:pdpu-participe'))
    
def vote_iframe(request, question_id):
  
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
    return HttpResponseRedirect(reverse('agora:home'))

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
    return HttpResponseRedirect(reverse('agora:home'))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return HttpResponseRedirect(reverse('agora:home'))


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
    return HttpResponseRedirect(reverse('agora:home'))

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
      return HttpResponseRedirect(reverse('agora:home'))
    else:
      messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:home'))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return HttpResponseRedirect(reverse('agora:home'))

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
    return HttpResponseRedirect(reverse('agora:pdpu'))

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
    return HttpResponseRedirect(reverse('agora:pdpu'))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return HttpResponseRedirect(reverse('agora:pdpu'))













def posvotacao(request):
  return render(request, 'agora/pos-votacao.html')
