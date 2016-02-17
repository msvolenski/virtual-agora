from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response,redirect
from django.views.generic.list import MultipleObjectMixin
from django.db.models import Max
from django.utils.decorators import method_decorator
from .models import Choice, Question, User, Answer
from django.db import models
from taggit.models import Tag
from django.contrib.auth.models import User as AuthUser
from django.contrib import messages


###############################################################################################
@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class HomeView(generic.ListView):
  template_name = 'agora/home.html'
  model= User

  def get_queryset(self):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    return Question.objects.filter(
      pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:2]
#################################################################################################3


@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class PdpuView(generic.ListView):
  
  template_name = 'agora/pagina-pdpu.html'

  def get_queryset(self):
      return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

##########################################################################################################


@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class PdpuParticipeView(generic.ListView):
  template_name = 'agora/pdpu-participe.html'
  model = Question
  #QuestoesRespondidas.objects.all().delete()
  def get_queryset(self):
   
    return Question.objects.filter(
      pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

  def get_context_data(self, **kwargs):
    context = super(PdpuParticipeView, self).get_context_data(**kwargs)

    user = User.objects.get(user=self.request.user)
    questions = Question.objects.filter(exp_date__gt=timezone.now())
    answered =  Answer.objects.filter(user_id=user.id)
    answered_questions = [a.question for a in answered]

    context['not_answered'] = list(set(questions) - set(answered_questions))
    return context

###############################################################################################################3

#@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
#class PdpuResultadosView(generic.ListView):
#  template_name = 'agora/pdpu-resultados.html'
#  model = Question
#
#  def get_queryset(self):
#    """
#    Return the last five published questions (not including those set to be
#    published in the future).
#    """
#    return Question.objects.filter(
#      pub_date__lte=timezone.now()
#    ).order_by('-pub_date')
#
#  def get_context_data(self, **kwargs):
#    context = super(PdpuResultadosView, self).get_context_data(**kwargs)
#    context['user_nome'] = self.request.user
#    context['q'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
#
#    return context

#####################################################################################################################
@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class PdpuComunidadeView(generic.ListView):
  template_name = 'agora/pdpu-comunidade.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    return Question.objects.filter(
      pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]
#########################################################################################################
    
@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class DetailView(generic.DetailView):
  model = Question
  template_name = 'agora/detail.html'


  

###############################################################################################################

@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class ResultsView(generic.DetailView):
  model = Question
  template_name = 'agora/result.html'

  def get_queryset(self):
    """
    Excludes any questions that aren't published yet.
    """
    return Question.objects.all()

  def get_context_data(self, **kwargs):
    context = super(ResultsView, self).get_context_data(**kwargs)
    context['user'] = User.objects.all()
    context['answered'] = Answer.objects.all()    
        
    ##RETIRAR#############################################################
    context['usuario'] = Usuario.objects.all()
    context['questoesrespondidas'] = QuestoesRespondidas.objects.all()
    context['votodousuario'] = VotoDoUsuario.objects.all()

    return context

#==================================================================================================
# O método a seguir processa o voto do usuário ao clicar em "votar" em questões de múltipla escolha
#==================================================================================================
#def vote(request, question_id):
#  question = get_object_or_404(Question, pk=question_id)
#  username = User.objects.get(username=request.user)
#
#  try:
#    question_type = question.question_type
#    if question_type == "1":
#      selected_choice = question.choice_set.get(pk=request.POST['choice'])
#    elif question_type == "2":
#      selected_choice = request.POST.getlist('choice')
#    elif question_type == "3":
#      selected_choice = request.POST['text']
#
#  except (KeyError, Choice.DoesNotExist):
#    # Redisplay the question voting form.
#    # Linha abaixo deleta o banco de dados de questões respondidas
#    #QuestoesRespondidas.objects.all().delete()
#    return render(request, 'agora/detail.html',
#      {
#        'question': question,
#        'error_message': 'bla',
#        'error_message': VotoDoUsuario.objects.filter(user__nome__startswith=username),
#      })
#
#  else:
#    # Abaixo são armazenadas as questões que o usuário votou. Os models são QuestoesRespondidas e Usuario
#    answered_question = QuestoesRespondidas.objects.filter(
#      usuario__nome__startswith=username,
#      questao__contains=str(question_id)
#    ).count()
#    if answered_question:
#      # return HttpResponseRedirect(reverse('agora:results', args=(question.id,)))
#      return HttpResponseRedirect(reverse('agora:posvotacao'))
#    else:
#      department = username.userprofile.faculdade
#
#      # Save the user
#      u1 = Usuario(nome=username)
#      u1.save()
#
#      # Save the answered question
#      q1 = QuestoesRespondidas(questao=str(question_id))
#      q1.save()
#      q1.usuario.add(u1)
#
#      # Save the vote
#      if question_type == "1" or question_type == "3":
#        q2 = VotoDoUsuario(
#          voto=selected_choice,
#          questao=str(question_id),
#          user=u1,
#          faculdade=department)
#        q2.save()
#      elif question_type == "2":
#        for element in selected_choice:
#          q2 = VotoDoUsuario(
#            voto=question.choice_set.get(pk=element),
#            questao=str(question_id),
#            user=u1,
#            faculdade=department)
#          q2.save()
#
#      return HttpResponseRedirect(reverse('agora:posvotacao'))

#################################################################################
def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type

  success = False

  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
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


































def posvotacao(request):
  return render(request, 'agora/pos-votacao.html')
