from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='portfolio'),
    path('add_operation/', views.OperationCreate.as_view(), name='add_operation'),
]