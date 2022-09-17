from django.shortcuts import render
from django.views.generic import CreateView
from .models import Portfolio, PortfolioStock
from .forms import OperationForm


def index(request):
    portfolio = Portfolio.objects.get(pk=1)
    stocks = PortfolioStock.objects.filter(portfolio=portfolio)
    return render(request, 'portfolio/index.html', {'stocks': stocks})


class OperationCreate(CreateView):
    form_class = OperationForm
    template_name = 'portfolio/add_transaction.html'
