from datetime import timedelta

from django.contrib.auth.models import User as AuthUser
from django.db import models
from django.utils import timezone

from taggit.managers import TaggableManager


class Question(models.Model):
  """Model for questions"""

  STATUS_CHOICES = (
    ('u', 'Não publicado'), # unpublished
    ('p', 'Publicado'),     # published
  )

  EXP_TIME = (
    (1, '1 dia'),           # a day
    (7, '1 semana'),        # a week
    (30, '1 mês'),          # a month
    (365, '1 ano'),         # a year
    (3650, 'Indeterminado') # undetermined
  )

  QUESTION_TYPE = (
    ('o', 'Única'),     # one
    ('m', 'Múltipla'),  # multiple
    ('t', 'Texto'),     # text
  )

  question_type = models.CharField('Tipo', max_length=1, choices=QUESTION_TYPE)
  question_text = models.CharField('Questão', max_length=200)
  pub_date = models.DateTimeField('Data de publicação')
  exp_date = models.DateTimeField('Data de expiração')
  days = models.IntegerField('Tempo para expirar', choices=EXP_TIME, default=3650)
  question_status = models.CharField('Estado da questão', max_length=1, choices=STATUS_CHOICES, default = 'p')
  answer_status = models.CharField('Estado da resposta', max_length=1, choices=STATUS_CHOICES, default = 'u')
  image = models.ImageField('Imagem', upload_to='question_images', blank=True, null=True)
  tags = TaggableManager()

  def __str__(self):
    if self.id:
      return "#{id} - {question}".format(id=self.id, question=self.question_text)
    else:
      return self.question_text

  def save(self, *args, **kwargs):
    """On save, update timestamps"""

    if not self.id:
      self.pub_date = timezone.now()
    self.update_expiration_time()
    return super(Question, self).save(*args, **kwargs)

  def update_expiration_time(self):
    self.exp_date = self.pub_date + timedelta(days=self.days)

  def is_question_expired(self):
    return self.exp_date <= timezone.now()

  def is_question_published(self):
    if self.is_question_expired():
      self.question_status = 'u'
    if self.question_status == 'p':
      return True
    else:
      return False

  is_question_published.boolean = True
  is_question_published.short_description = 'Publicada?'

  def is_answer_published(self):
    if self.answer_status == 'p':
      return True
    else:
      return False

  is_answer_published.boolean = True
  is_answer_published.short_description = 'Respostas publicadas?'

  class Meta:
    verbose_name = 'questão'
    verbose_name_plural = 'questões'


class Choice(models.Model):
  """Model for choices of a question"""

  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)

  def __str__(self):
    return self.choice_text

  class Meta:
    verbose_name = 'escolha'
    verbose_name_plural = 'escolhas'


class User(models.Model):
  """Information about the registered user"""

  user = models.OneToOneField(
    AuthUser,
    primary_key=True,
    parent_link=True,
  )

  year_of_start = models.IntegerField(blank=True)
  department = models.CharField(max_length=40, blank=True)
  course = models.CharField(max_length=40, blank=True)

  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  academic_registry = models.IntegerField(default=0)

  question_answer = models.ManyToManyField(
    Question,
    through='Answer',
    through_fields=('user', 'question'),
    related_name='question_answer',
  )

  def __str__(self):
    return self.first_name + ' ' + self.last_name

  class Meta:
    verbose_name = 'usuário'
    verbose_name_plural = 'usuários'


class Answer(models.Model):
  """Answer to a question"""

  user = models.ForeignKey(User)
  question = models.ForeignKey(Question)
  choice = models.ForeignKey(Choice, blank=True, null=True)
  text = models.TextField(max_length=200, blank=True, null=True)
  answer_date = models.DateTimeField(editable=False)

  def __str__(self):
    if self.choice:
      return self.choice.choice_text
    return self.text

  def save(self, *args, **kwargs):
    """On save, update timestamps"""

    if not self.id:
      self.answer_date = timezone.now()
    return super(Answer, self).save(*args, **kwargs)

  def user_dept(self):
    return self.user.department
  user_dept.short_description = 'Faculdade'

  class Meta:
    verbose_name = 'resposta'
    verbose_name_plural = 'respostas'
