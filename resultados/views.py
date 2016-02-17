from django.views.generic import ListView
from .models import Relatorio, Likedislike
#from agora.models import QuestoesRespondidas
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext, Context, loader


# Create your views here.




@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class TemplatePDPUResultadosView(ListView):
    model = Relatorio
    
    
    #def get_context_data(self, **kwargs):
        #context = super(TemplatePDPUConhecaView, self).get_context_data(**kwargs)     
        #context['question'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
        #context['link'] = Link.objects.all()
        #context['topico'] = Topico.objects.all().order_by('position')
        #return context
        
    def get_queryset(self):
        return Relatorio.objects.all().order_by('-publ_date')
        
@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')        
class RelatorioPageView(generic.DetailView):
    model = Relatorio       
    template_name = 'resultados/relatorio_page.html'
    
    def get_queryset(self):
        return Relatorio.objects.all()    
        
    #def get_context_data(self, **kwargs):
     #   context = super(ArticlePageView, self).get_context_data(**kwargs)     
      #  context['question'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
       # return context 
        
##@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')        
##class ArticlePageView(generic.DetailView):
#    model = Article       
#    template_name = 'conheca/article_page.html'
#    
#    def get_queryset(self):
#        return Article.objects.all()    
#        
#    def get_context_data(self, **kwargs):
#        context = super(ArticlePageView, self).get_context_data(**kwargs)     
#        context['question'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
#        return context
#        
#@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')        
#class ArticleDestaquePageView(generic.DetailView):
#    model = Article       
#    template_name = 'conheca/article_destaque_page.html'
#    
#    def get_queryset(self):
#        return Article.objects.all()    
#        
#    def get_context_data(self, **kwargs):
#        context = super(ArticleDestaquePageView, self).get_context_data(**kwargs)     
#        context['question'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
#        return context
#        
#        
#class TopicoPageView(generic.DetailView):
#    model = Topico       
#    template_name = 'conheca/topico_page.html'
#    
#    def get_queryset(self):
#        return Topico.objects.all()    
#        

def like(request, relatorio_id):
    relatorio = get_object_or_404(Relatorio, pk=relatorio_id)    
    try:
        obj = Likedislike.objects.get(user=request.user, relatorio=relatorio_id)
    except Likedislike.DoesNotExist:
            obj = Likedislike(user=request.user, relatorio=relatorio_id)
            obj.save()    
            relatorio.like += 1
            relatorio.save()
            return HttpResponseRedirect(reverse('resultados:relatorio_page', args=(relatorio.id,))) 
    return HttpResponseRedirect(reverse('resultados:relatorio_page', args=(relatorio.id,)))
  
def dislike(request, relatorio_id):   
    relatorio = get_object_or_404(Relatorio, pk=relatorio_id)    
    try:
        obj = Likedislike.objects.get(user=request.user, relatorio=relatorio_id)
    except Likedislike.DoesNotExist:
            obj = Likedislike(user=request.user, relatorio=relatorio_id)
            obj.save()    
            relatorio.dislike += 1
            relatorio.save()
            return HttpResponseRedirect(reverse('resultados:relatorio_page', args=(relatorio.id,))) 
    return HttpResponseRedirect(reverse('resultados:relatorio_page', args=(relatorio.id,)))
    
    
def search_res(request):
  
    tags_user = request.POST['q'].split(' ')
    relatorio = Relatorio.objects.filter(tags__name__in=tags_user).distinct()
    tags_total=len(tags_user)   
    return render(request, 'resultados/search_result_res.html', 
      {
        'relatorio': relatorio,
        'tags_user': tags_user,
        'tags_total': tags_total
      })                    
        
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    















#def likedislike(request, relatorio_id):
#    relatorio = get_object_or_404(Relatorio, pk=relatorio_id)
#    username = User.objects.get(username=request.user)    
#    
#    
#    new_like, created = LikeDislike.objects.get_or_create(user=request.user, relatorio_id=relatorio_id) 
#    if not created:
#        return
#    else:
#        new_like.save()            
#        selected_like = request.POST['like']         
#        selected_dislike = request.POST['dislike']
#        
#        if selected_like == "1":
#            add = LikeDislike.get(pk=relatorio_id)
#            add.like += 1
#            add.save()
#        if selected_dislike == "1":
#            add = LikeDislike.get(pk=relatorio_id)
#            add.dislike += 1
#            add.save()
#        return


 # Save the user
     




#
#def search(request):
#  
#    tags_user = request.POST['q'].split(' ')
#    articles = Article.objects.filter(tags__name__in=tags_user).distinct()
#    tags_total=len(tags_user)   
#    return render(request, 'conheca/search_result.html', 
#      {
#        'article': articles,
#        'tags_user': tags_user,
#        'tags_total': tags_total
#      })
