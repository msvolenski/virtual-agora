from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from agora.models import Question
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import User

class Relatorio(models.Model):

    TIPOS = (
        ('1', 'Geral'),
        ('2', 'Questão'),
    )
    questao = models.ForeignKey(Question,blank=True, null=True)
    tags = TaggableManager()
    tipo = destaque = models.CharField(max_length=10, choices=TIPOS, default='1')
    titulo =  models.CharField(max_length=100)
    conteudo = RichTextUploadingField(config_name='full', verbose_name=u'Resultado e Análise')
    publ_date = models.DateTimeField(null=True)
    destaque = models.CharField(max_length=3, default='Não')
    address = models.CharField(max_length=200)
    published = models.CharField(max_length=3, default='Não')
    publhistorico = models.CharField(max_length=3, default='Não')
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __int__(self):
        return self.questao.id

    def save(self, *args, **kwargs):
        super(Relatorio, self).save(*args, **kwargs)
        self.address = "http://127.0.0.1:8000/agora/pdpu/resultados/relatorio/{id}".format(id=self.id)
        return super(Relatorio, self).save(*args, **kwargs)

class Likedislike(models.Model):
    user = models.CharField(max_length=30)
    relatorio = models.IntegerField()
