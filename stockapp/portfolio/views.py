from django.shortcuts import render
from .models import Portfolio, PortfolioStock


def index(request):
    portfolio = Portfolio.objects.get(pk=1)
    stocks = PortfolioStock.objects.filter(portfolio=portfolio)
    return render(request, 'portfolio/index.html', {'stocks': stocks})
