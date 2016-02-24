from django.contrib import messages
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User as AuthUser

from agora.models import User as QuestionUser
from .models import Category, Topic, TopicAnswer, User, TopicAnswerForm



@method_decorator(login_required(login_url='agora:login'), name='dispatch')
class ForumHomeView(generic.ListView):
  """Homepage of the forum"""

  template_name = 'forum/home.html'
  model = Category
  context_object_name = 'categories_list'


@method_decorator(login_required(login_url='agora:login'), name='dispatch')
class ForumView(generic.ListView):
  """Show all the categories of the forum"""

  template_name = 'forum/forum.html'
  model = Category

  def get_context_data(self, **kwargs):
    context = super(ForumView, self).get_context_data(**kwargs)
    context['category'] = Category.objects.get(id=self.kwargs['pk'])
    context['topics_list'] = Topic.objects.filter(category=context['category'])
    return context


@method_decorator(login_required(login_url='agora:login'), name='dispatch')
class TopicView(generic.ListView):
  """Show all topics in a category"""

  template_name = 'forum/topic.html'
  model = Topic

  def get_context_data(self, **kwargs):
    context = super(TopicView, self).get_context_data(**kwargs)
    context['topic'] = Topic.objects.get(id=self.kwargs['pk'])
    context['answers'] = TopicAnswer.objects.filter(topic=context['topic']).order_by('-answer_date').reverse()
    context['answer_form'] = TopicAnswerForm()
    # context['answer_form'] = modelformset_factory(TopicAnswer, fields=['text'])

    auth_user = self.request.user
    user = auth_user.user
    context['req_user'] = self.request.user
    context['username'] = auth_user
    context['user'] = user
    context['topic_user'] = User.objects.get(user=auth_user)

    if TopicAnswer.objects.filter(user=context['topic_user'], topic=context['topic']).count():
      context['user_answered'] = True
    else:
      context['user_answered'] = False

    return context


def save_topic_answer(request, topic_id):
  """Save the answer of the user"""

  topic = get_object_or_404(Topic, pk=topic_id)
  auth_user = AuthUser.objects.get(username=request.user)
  topic_user = User.objects.get(user=auth_user)


  # Query over the voted questions
  answered_topic = TopicAnswer.objects.filter(user=topic_user, topic=topic).count()
  if answered_topic:
    error_message = 'Você já respondeu este tópico.'
    messages.error(request, error_message)
  else:
    # Save the answer
    answer = request.POST['text']
    if answer:
      answer_model = TopicAnswer(user=topic_user, topic=topic, text=answer)
      answer_model.save()
      messages.success(request, "Obrigado por participar!")
    else:
      messages.error(request, "Parece que você deixou o campo em branco. Por favor, tente novamente.")

  return HttpResponseRedirect(reverse('forum:topic', kwargs={'pk': topic_id}))
