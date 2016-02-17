from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

from .models import Category, Topic


@method_decorator(login_required(login_url='agora:login'), name='dispatch')
class ForumHomeView(generic.ListView):
  template_name = 'forum/home.html'
  model = Category
  context_object_name = 'categories_list'


@method_decorator(login_required(login_url='agora:login'), name='dispatch')
class ForumView(generic.ListView):
  template_name = 'forum/forum.html'
  model = Category

  def get_context_data(self, **kwargs):
    context = super(ForumView, self).get_context_data(**kwargs)
    context['category'] = Category.objects.get(id=self.kwargs['pk'])
    context['topics_list'] = Topic.objects.filter(category=context['category'])
    return context


# @method_decorator(login_required(login_url='agora:login'), name='dispatch')
# class TopicView(generic.ListView):
#   template_name = 'forum/topic.html'
#   model = Topic
