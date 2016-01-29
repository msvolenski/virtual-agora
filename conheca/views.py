from django.views.generic import ListView
from .models import AdicionaLink, Article
from agora.models import QuestoesRespondidas
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.




@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class TemplatePDPUConhecaView(ListView):
    model = Article
    
    
    def get_context_data(self, **kwargs):
        context = super(TemplatePDPUConhecaView, self).get_context_data(**kwargs)     
        context['question'] = QuestoesRespondidas.objects.filter(usuario__nome__startswith=self.request.user).values()
        return context