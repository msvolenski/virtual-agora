from django.views.generic import ListView
from .models import SubTopico, Article, Link, Topico
from agora.models import Answer, User, Question
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext, Context, loader
from django.contrib.auth.models import User as AuthUser
from django.utils import timezone


# Create your views here.




@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class TemplatePDPUConhecaView(ListView):
    model = Article
    
    
    def get_context_data(self, **kwargs):
        context = super(TemplatePDPUConhecaView, self).get_context_data(**kwargs)     
        #context['question'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
        context['link'] = Link.objects.all()
        context['topico'] = Topico.objects.all().order_by('position')
        return context
        
    def get_queryset(self):
        return Article.objects.all().order_by('-publ_date')
        
  
        
@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')        
class ArticlePageView(generic.DetailView):
    model = Article       
    template_name = 'conheca/article_page.html'
    
    def get_queryset(self):
        return Article.objects.all()    
        
    def get_context_data(self, **kwargs):
        context = super(ArticlePageView, self).get_context_data(**kwargs)     
        #context['question'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
        user = User.objects.get(user=self.request.user)
        questions = Question.objects.filter(exp_date__gt=timezone.now())
        answered =  Answer.objects.filter(user_id=user.id)
        answered_questions = [a.question for a in answered]
        context['not_answered'] = list(set(questions) - set(answered_questions))       
        return context        
        
        
@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')        
class ArticleDestaquePageView(generic.DetailView):
    model = Article       
    template_name = 'conheca/article_destaque_page.html'
    
    def get_queryset(self):
        return Article.objects.all()    
        
    def get_context_data(self, **kwargs):
        context = super(ArticleDestaquePageView, self).get_context_data(**kwargs)     
        #context['question'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
        user = User.objects.get(user=self.request.user)
        questions = Question.objects.filter(exp_date__gt=timezone.now())
        answered =  Answer.objects.filter(user_id=user.id)
        answered_questions = [a.question for a in answered]
        context['not_answered'] = list(set(questions) - set(answered_questions))       
        return context  
        
        
class TopicoPageView(generic.DetailView):
    model = Topico       
    template_name = 'conheca/topico_page.html'
    
    def get_queryset(self):
        return Topico.objects.all()    
        
   


def search(request):
  
    tags_user = request.POST['q'].split(' ')
    articles = Article.objects.filter(tags__name__in=tags_user).distinct()
    tags_total=len(tags_user)   
    return render(request, 'conheca/search_result.html', 
      {
        'article': articles,
        'tags_user': tags_user,
        'tags_total': tags_total
      })


  