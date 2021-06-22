from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.views.generic import ListView, DetailView
from django.utils import timezone



class PoolsIndexView(ListView):
   context_object_name = 'latest_question_list'
   template_name = 'pools/pools_index.html'
   
   def get_queryset(self):
       query_set = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:]
       return query_set

class PoolsDetailView(DetailView):
    model = Question
    template_name = 'pools/pools_detail.html'


class PoolsResultsView(DetailView):
    model = Question
    template_name = 'pools/pools_results.html'


def pools_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'pools/pools_detail.html', 
        {'question':question, 'error_message': 'You did not select a choice'})
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('pools_results', args=(question_id,)))
