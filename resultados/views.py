from django.views.generic import ListView
from .models import Relatorio, Likedislike
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext, Context, loader
from agoraunicamp.decorators import term_required
from agora.models import Choice, Question, InitialListQuestion
from agoraunicamp.models import User, Answer, Termo, Tutorial
from projetos.models import Projeto


#PROJETO
@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class ResultadosView(ListView):
    model = Relatorio

    def get_queryset(self):
        u = User.objects.get(user=self.request.user)
        return Relatorio.objects.filter(published='Sim',projeto__sigla=u.projeto).order_by('-publ_date')

    def get_context_data(self, **kwargs):
        context = super(ResultadosView, self).get_context_data(**kwargs)
        user = User.objects.get(user=self.request.user)
        projeto_nome = Projeto.objects.filter(sigla=user.projeto).first()
        t = Tutorial.objects.get(user=user)
        context['tutorial'] = t.status
        context['projeto'] = projeto_nome.projeto
        context['sigla'] = user.projeto
        context['relatorio_hist_1'] =  Relatorio.objects.filter(publhistorico='Sim',tipo='1',projeto__sigla=user.projeto).order_by('-publ_date')
        context['relatorio_hist_2'] =  Relatorio.objects.filter(publhistorico='Sim',tipo='2',projeto__sigla=user.projeto).order_by('-publ_date')
        context['nickname'] = user.nickname
        return context


@method_decorator(login_required(login_url='agoraunicamp:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class RelatorioPageView(generic.DetailView):
    model = Relatorio
    template_name = 'resultados/relatorio_page.html'

    def get_context_data(self, **kwargs):
        context = super(RelatorioPageView, self).get_context_data(**kwargs)
        user = User.objects.get(user=self.request.user)
        context['nickname'] = user.nickname
        return context

    def get_queryset(self):
        return Relatorio.objects.all()


def like(request, relatorio_id):
    relatorio = get_object_or_404(Relatorio, pk=relatorio_id)
    try:
        obj = Likedislike.objects.get(user=request.user, relatorio=relatorio_id)
    except Likedislike.DoesNotExist:
            obj = Likedislike(user=request.user, relatorio=relatorio_id)
            obj.save()
            relatorio.like += 1
            relatorio.save()
            return redirect(request.META['HTTP_REFERER']+"#relatorio%s"%(relatorio_id))
    return redirect(request.META['HTTP_REFERER']+"#relatorio%s"%(relatorio_id))

def dislike(request, relatorio_id):
    relatorio = get_object_or_404(Relatorio, pk=relatorio_id)
    try:
        obj = Likedislike.objects.get(user=request.user, relatorio=relatorio_id)
    except Likedislike.DoesNotExist:
            obj = Likedislike(user=request.user, relatorio=relatorio_id)
            obj.save()
            relatorio.dislike += 1
            relatorio.save()
            #return redirect(request.META['HTTP_REFERER']+"#relatorio%s"%(relatorio_id))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')+"#relatorio%s"%(relatorio_id))
    #return redirect(request.META['HTTP_REFERER']+"#relatorio%s"%(relatorio_id))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')+"#relatorio%s"%(relatorio_id))
