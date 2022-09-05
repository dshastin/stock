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


class PortfolioStockAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'stock', 'total_amount', 'average_price']
    list_filter = ['portfolio']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['get_owner', 'portfolio', 'stock', 'order', 'price', 'amount']

    @admin.display(description='Владелец')
    def get_owner(self, obj):
        return obj.portfolio.owner

    def delete_queryset(self, request, queryset):
        print(queryset)
        for q in queryset:
            print(q)
            super(TransactionAdmin, self).delete_queryset(request, q)
            print(q)
            q.portfolio.update_balance(q.stock)



admin.site.register(Segment, SegmentAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Operation, TransactionAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PortfolioStock, PortfolioStockAdmin)
