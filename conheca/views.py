from django.views.generic import ListView
from .models import Topic, Article, Link
from agora.models import QuestoesRespondidas
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic

# Create your views here.




@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class TemplatePDPUConhecaView(ListView):
    model = Article
    
    
    def get_context_data(self, **kwargs):
        context = super(TemplatePDPUConhecaView, self).get_context_data(**kwargs)     
        context['question'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
        context['link'] = Link.objects.all()
        context['topic'] = Topic.objects.all().order_by('position')
        return context
        
  
        
@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')        
class ArticlePageView(generic.DetailView):
    model = Article       
    template_name = 'conheca/article_page.html'
    
    def get_queryset(self):
        return Article.objects.all()    
        
    def get_context_data(self, **kwargs):
        context = super(ArticlePageView, self).get_context_data(**kwargs)     
        context['question'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
        return context
        
    
    