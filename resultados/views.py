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

@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class TemplatePDPUResultadosView(ListView):
    model = Relatorio

    def get_queryset(self):
        return Relatorio.objects.filter(published='Sim').order_by('-publ_date')

    def get_context_data(self, **kwargs):
        context = super(TemplatePDPUResultadosView, self).get_context_data(**kwargs)
        context['relatorio_hist_1'] =  Relatorio.objects.filter(publhistorico='Sim',tipo='1').order_by('-publ_date')
        context['relatorio_hist_2'] =  Relatorio.objects.filter(publhistorico='Sim',tipo='2').order_by('-publ_date')
        return context


@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class RelatorioPageView(generic.DetailView):
    model = Relatorio
    template_name = 'resultados/relatorio_page.html'

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
