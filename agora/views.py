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
from .models import Choice, Question, QuestoesRespondidas, Usuario, VotoDoUsuario, UserProfile
from django.contrib.auth.models import User
from django.db import models
from taggit.models import Tag
from conheca.models import AdicionaLink

#==============================================================================
# @method_decorator(login_required(login_url='/agora/login/') DEVE SER COLOCADO EM TODAS AS VIEWS NÃO PÚBLICAS!
#==============================================================================

@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class HomeView(generic.ListView): 
    template_name = 'agora/home.html'
      
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:2]

#==============================================================================
# VIEW DA PÁGINA PRINCIPAL DO PLANO DIRETOR PARTICIPATIVO DA UNICAMP 
# Basicamente atualiza as timelines das quatros partes: Conheça, Participe, Resultados e Comunidade
#==============================================================================
@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class PdpuView(generic.ListView):
   
    template_name = 'agora/pagina-pdpu.html'
    model = AdicionaLink
    #context_object_name = 'Question_list'
    #Configura quantos links serQo mostrados na ordem da data de publicação 
    
    
    #Contém os outros objetos além de "AdicionaLink": Question, ...    
    def get_context_data(self, **kwargs):
        context = super(PdpuView, self).get_context_data(**kwargs)
        context['Question'] = Question.objects.filter( #Label 'Question" deve ser usada no template
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:4]
        context['tag'] = Tag.objects.all()   
        context['user_nome'] = self.request.user
        context['q'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()        
        #número que define quantas "Questions" vão aparecer       
        return context     
    
    #Retorna para o template o objeto principal: AdicionaLink
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return AdicionaLink.objects.filter(
            data_publicacao__lte=timezone.now()
        ).order_by('-data_publicacao')[:4] 
        
    
    
#@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
#lass TemplatePDPUConhecaView(ListView):
    #model = AdicionaLink
        
        

#==============================================================================
# A classe abaixo cria a "timeline" de questões na Página PDPU - PARTICIPE
#==============================================================================
@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class PdpuParticipeView(generic.ListView):
    template_name = 'agora/pdpu-participe.html'
    model = Question
    #QuestoesRespondidas.objects.all().delete()     
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super(PdpuParticipeView, self).get_context_data(**kwargs)
        context['user_nome'] = self.request.user
        context['q'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
        context['tag'] = Question.tags.all() 
        return context    
 
   


@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class PdpuResultadosView(generic.ListView):
    template_name = 'agora/pdpu-resultados.html'
    model = Question

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).

        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
        
    def get_context_data(self, **kwargs):
        context = super(PdpuResultadosView, self).get_context_data(**kwargs)
        context['user_nome'] = self.request.user
        context['q'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
      
        return context   
        
        
        
        
        
        
        
        
        

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




@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class DetailView(generic.DetailView):
    model = Question
    template_name = 'agora/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

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
        context['usuario'] = Usuario.objects.all()
        context['questoesrespondidas'] = QuestoesRespondidas.objects.all()
        context['votodousuario'] = VotoDoUsuario.objects.all()
               
         
        return context

#==================================================================================================
# O método a seguir processa o voto do usuário ao clicar em "votar" em questões de múltipla escolha
#==================================================================================================
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
       
    try:
        if question.question_type == "1":             
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        if question.question_type == "2":        
            selected_choice = request.POST.getlist('choice')
        if question.question_type == "3": 
            selected_choice = request.POST['text']    
    
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        # Linha abaixo deleta o banco de dados de questões respondidas
        #QuestoesRespondidas.objects.all().delete()  
        user_nome = User.objects.get(username = request.user)        
        return render(request, 'agora/detail.html', {
            'question': question,
            'error_message': 'bla',                      
            'error_message': VotoDoUsuario.objects.filter(user__nome__startswith=user_nome) ,  
                
        })
    else:
           
           #Abaixo são armazenadas as questões que o usuário votou. Os models são QuestoesRespondidas e Usuario 
            user_nome = User.objects.get(username = request.user)
            a = QuestoesRespondidas.objects.filter(usuario__nome__startswith=user_nome, questao__contains=str(question_id)).count()        
            if a != 0:
                #return HttpResponseRedirect(reverse('agora:results', args=(question.id,)))
                return HttpResponseRedirect(reverse('agora:posvotacao')) 
            else:                           
                
                #salva atributos do usuario
    
                u = User.objects.get(username = request.user)             
                faculdade1 = u.userprofile.faculdade          
                                       
                #salvam o usuário, a questão respondida e o voto no DB     
                u1 = Usuario(nome=user_nome)                       
                u1.save()
               
                q1 = QuestoesRespondidas(questao=str(question_id))          
                q1.save()  
                q1.usuario.add(u1)
                
                if question.question_type == "1":
                    selected_choice.votes += 1
                    selected_choice.save()    
                    text = selected_choice.choice_text
                    u2 = Usuario(nome=user_nome)           
                    u2.save()            
                    q2 = VotoDoUsuario(voto=text,questao=str(question_id), user=u2, faculdade=faculdade1)  
                    q2.save() 
                
                if question.question_type == "3":
                    text = selected_choice
                    u2 = Usuario(nome=user_nome)           
                    u2.save()            
                    q2 = VotoDoUsuario(voto=text,questao=str(question_id), user=u2, faculdade=faculdade1)  
                    q2.save()                
                            
                if question.question_type == "2":
                    for element in selected_choice:                     
                        text = question.choice_set.get(pk=element)                        
                        u2 = Usuario(nome=user_nome)           
                        u2.save()            
                        q2 = VotoDoUsuario(voto=text,questao=str(question_id), user=u2, faculdade=faculdade1)  
                        q2.save()               
                
                
                              
                   
                return HttpResponseRedirect(reverse('agora:posvotacao'))

    






def posvotacao(request):
    return render(request, 'agora/pos-votacao.html')
      
