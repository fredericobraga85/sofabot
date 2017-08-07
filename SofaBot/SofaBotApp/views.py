from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.shortcuts import render_to_response, redirect
from django.http import JsonResponse
from .models import Exchange, OrderState, Question, Choice
from utils import TickerThread
from django.utils import timezone
from django.contrib import messages
import json
import pdb;

class IndexView(generic.ListView):

    template_name = 'SofaBotApp/index.html'
    context_object_name = 'exchange_list'


    def get_queryset(self):



        return Exchange.objects.order_by('id')[:]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        dict = {}
        for key, value in TickerThread.thread1.p.returnBalances().iteritems():

            if key == "BTC":
                context['btc_max'] = value
                dict[key] = value
            elif float(value) > 0:
                dict[key] = value

        context['wallets'] = dict

        dict_coin = {}
        for key, value in TickerThread.thread1.p.returnTicker().iteritems():

            if  "BTC" in key:
                dict_coin[key] = value

        context['coins'] = dict_coin
        context['success_message'] = self.request.session.get('success_message')  # get the value from session
        context['error_message'] = self.request.session.get('error_message')  # get the value from session
        self.request.session['error_message'] = None
        self.request.session['success_message'] = None

        return context


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

    return JsonResponse(TickerThread.thread1.resp_dict)

def addBot(request):

    currency_pair = request.POST['currency_pair']
    initial_btc = request.POST['initial_btc']

    try:
        e = Exchange.objects.get(currency_pair=currency_pair)

        request.session['error_message'] =  currency_pair + " ja foi adicionado."
        return redirect("/SofaBotApp/")

    except Exchange.DoesNotExist:
        e = Exchange(currency_pair= currency_pair, initial_btc= initial_btc)
        e.save()
        e.orderstate_set.create(state_date=timezone.now(), current_btc=initial_btc)
        e.save()

        request.session['success_message'] = currency_pair + " adicionado com sucesso."
        return redirect("/SofaBotApp/")

    except Exception as ex:

        print  ex

        request.session['error_message'] = "Ocorreu um erro ao adicionar " + currency_pair
        return redirect("/SofaBotApp/")

def startExchange(request, exchange_id):

    try:
        e = get_object_or_404(Exchange, pk=exchange_id)
        e.isActive = True
        e.save()

        request.session['success_message'] = e.currency_pair + " iniciado com sucesso."
        return redirect("/SofaBotApp/")

    except Exception as ex:

        request.session['error_message'] = "Ocorreu um erro ao iniciar"
        return redirect("/SofaBotApp/")

def stopExchange(request, exchange_id):

    try:
        e = get_object_or_404(Exchange, pk=exchange_id)
        e.isActive = False
        e.save()

        request.session['success_message'] = e.currency_pair + " parado com sucesso."
        return redirect("/SofaBotApp/")

    except Exception as ex:

        request.session['error_message'] = "Ocorreu um erro ao parar"
        return redirect("/SofaBotApp/")

