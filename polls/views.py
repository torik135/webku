from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'q_terakhir'
  paginate_by = 2

  def get_queryset(self):
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
  model = Question
  context_object_name = 'q'
  template_name = 'polls/detail.html'

  def get_queryset(self):
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    )


class ResultsView(generic.DetailView):
  model = Question
  context_object_name = 'q'
  template_name = 'polls/results.html'


def vote(request, question_id):
  q = get_object_or_404(Question, pk=question_id)
  try:
    s_choice = q.choice_set.get(pk=request.POST['c'])
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/detail.html', {
        'q': q,
        'error_message': 'tidak pilih choice',
    })
  else:
    s_choice.votes += 1
    s_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(q.id,)))
