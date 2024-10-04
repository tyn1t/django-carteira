from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "tes/index.html"
    context_name = "latest_question_list"
    
    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "tes/detail.html"

    
class ResultsView(generic.DetailView):
    model = Question
    template_name = "tes/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "tes/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice,",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        
    return HttpResponseRedirect(reverse("tes:results", args=(question.id,)))