from django.db import models
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

    class Meta:
        verbose_name = 'Портфель'
        verbose_name_plural = 'Портфели'


class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('portfolio', 'stock'), )

    def get_balance(self):
        transactions = Transaction.objects.filter(portoflio=self)
        total_stock = 0
        for t in transactions:
            total_stock += t.amount * t.order.multiplier
        return total_stock


class Order(models.Model):
    title = models.CharField(max_length=50, verbose_name='Тип ордера')
    name = models.CharField(max_length=10, verbose_name='Код ордера')
    multiplier = models.IntegerField(verbose_name='Множитель операции')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип ордера'
        verbose_name_plural = 'Типы ордера'


class Transaction(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT, verbose_name='Портфель')
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, verbose_name='Акция')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Тип ордера')
    amount = models.IntegerField(verbose_name='Количество')
    price = models.FloatField(verbose_name='Цена')
    datetime = models.DateField(verbose_name='Дата')

    def __str__(self):
        return f'{self.order} {self.stock}: {self.amount} шт.'

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
