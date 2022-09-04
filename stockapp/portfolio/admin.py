from django.contrib import admin
from .models import *


class SegmentAdmin(admin.ModelAdmin):
    list_display = ['title']


class StockAdmin(admin.ModelAdmin):
    list_display = ['title', 'segment',]
    list_filter = ['segment', ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ['title']


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner']
    list_filter = ['owner']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['get_owner', 'portfolio', 'stock', 'order', 'price', 'amount']

    @admin.display(description='Владелец')
    def get_owner(self, obj):
        return obj.portfolio.owner


admin.site.register(Segment, SegmentAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Order, OrderAdmin)
