from django.views.generic import ListView
from .models import AdicionaLink
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.




@method_decorator(login_required(login_url='/agora/login/'), name='dispatch')
class TemplatePDPUConhecaView(ListView):
    model = AdicionaLink