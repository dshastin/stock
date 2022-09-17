from django.db import models
from django.db.models import Sum
# from django.contrib.auth.models import User


class Segment(models.Model):
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сегмент'
        verbose_name_plural = 'Сегменты'


class Stock(models.Model):
    title = models.CharField(max_length=255)
    ticker = models.CharField(max_length=5)
    segment = models.ForeignKey(Segment, on_delete=models.PROTECT, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'


class Portfolio(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название портфеля')
    owner = models.CharField(max_length=100, verbose_name='Владелец')
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def calc_stock_balance(self, stock):
        print(self.pk)
        portfolio_stock, created = PortfolioStock.objects.get_or_create(portfolio=self, stock=stock)

        total_stock_amount = 0
        total_stock_sum = 0
        for operation in self.operations.filter(stock=stock).filter(order__name='buy'):
            total_stock_amount += operation.amount
            total_stock_sum += operation.amount * operation.price

        if total_stock_amount == 0:
            portfolio_stock.delete()
        else:
            portfolio_stock.total_amount = total_stock_amount
            portfolio_stock.average_price = total_stock_sum / total_stock_amount
            portfolio_stock.save()

    def update_balance(self, stock=None):
        if stock:
            self.calc_stock_balance(stock)
        else:
            for stock in self.operations.values_list('stock__pk', flat=True).distinct():
                self.calc_stock_balance(stock)

    class Meta:
        verbose_name = 'Портфель'
        verbose_name_plural = 'Портфели'


class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='portfolio_stock')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    total_amount = models.IntegerField(default=0)
    average_price = models.FloatField(default=0)

    @property
    def total_sum(self):
        return self.total_amount * self.average_price

    def __str__(self):
        return f'{self.stock.ticker}: {self.total_amount}'

    class Meta:
        unique_together = (('portfolio', 'stock'), )


class Order(models.Model):
    title = models.CharField(max_length=50, verbose_name='Тип ордера')
    name = models.CharField(max_length=10, verbose_name='Код ордера')
    multiplier = models.IntegerField(verbose_name='Множитель операции')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип ордера'
        verbose_name_plural = 'Типы ордера'


class Operation(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, verbose_name='Портфель', related_name='operations')
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, verbose_name='Инструмент')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Тип ордера')
    amount = models.IntegerField(verbose_name='Количество')
    price = models.FloatField(verbose_name='Цена')
    datetime = models.DateField(verbose_name='Дата')

    def __str__(self):
        return f'{self.order} {self.stock}: {self.amount} шт.'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.portfolio.update_balance(self.stock)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.portfolio.update_balance(self.stock)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'