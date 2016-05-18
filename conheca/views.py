from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as AuthUser
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext, Context, loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import ListView
from .models import SubTopico, Article, Topico
from agora.models import Question
from agoraunicamp.decorators import term_required
from agoraunicamp.models import User, Answer, Tutorial
from projetos.models import Projeto

#PROJETO
@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class ConhecaView(ListView):
  model = Article

  def get_context_data(self, **kwargs):
    context = super(ConhecaView, self).get_context_data(**kwargs)
    #context['question'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
    user = User.objects.get(user=self.request.user)
    context['topico'] = Topico.objects.filter(projeto__sigla=user.projeto).order_by('position')
    questions = Question.objects.filter(exp_date__gt=timezone.now(),question_status='p')
    answered =  Answer.objects.filter(user_id=self.request.user.id)
    answered_questions = [a.question for a in answered]
    projeto_nome = Projeto.objects.filter(sigla=user.projeto).first()
    t = Tutorial.objects.get(user=user)
    context['tutorial'] = t.status
    context['projeto'] = projeto_nome.projeto
    context['sigla'] = user.projeto
    context['not_answered'] = list(set(questions) - set(answered_questions))
    context['nickname'] = user.nickname

    return context

  def get_queryset(self):
    u = User.objects.get(user=self.request.user)
    return Article.objects.filter(projeto__sigla=u.projeto).order_by('-publ_date')



#PROJETO
@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class ArticlePageView(generic.DetailView):
  model = Article
  template_name = 'conheca/article_page.html'

  def get_queryset(self):
    return Article.objects.all()

  def get_context_data(self, **kwargs):
    context = super(ArticlePageView, self).get_context_data(**kwargs)
    #context['question'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
    user = User.objects.get(user=self.request.user)
    questions = Question.objects.filter(exp_date__gt=timezone.now(),question_status='p')
    answered =  Answer.objects.filter(user_id=self.request.user.id)
    answered_questions = [a.question for a in answered]
    context['not_answered'] = list(set(questions) - set(answered_questions))
    context['nickname'] = user.nickname
    return context
