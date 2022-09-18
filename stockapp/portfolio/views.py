from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from .models import Portfolio, PortfolioStock, Operation
from .forms import OperationForm


def index(request):
    portfolio = Portfolio.objects.get(pk=1)
    stocks = PortfolioStock.objects.filter(portfolio=portfolio)
    return render(request, 'portfolio/index.html', {'stocks': stocks})


class OperationCreate(CreateView):
    form_class = OperationForm
    template_name = 'portfolio/add_operation.html'
    success_url = reverse_lazy('operations')


class OperationList(ListView):
    model = Operation
    template_name = 'portfolio/operations_list.html'
    context_object_name = 'operations'

    ordering = ['-datetime']
