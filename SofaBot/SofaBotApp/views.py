from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.shortcuts import render_to_response
from django.http import JsonResponse
from .models import Choice, Question
from utils import TickerThread
import json

class IndexView(generic.ListView):

    template_name = 'SofaBotApp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'SofaBotApp/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'SofaBotApp/results.html'


def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'SofaBotApp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(question.id,)))


def updateActualValue(request):

    data = {}
    data['actualValue'] = TickerThread.thread1.df['last']
    return JsonResponse(data)