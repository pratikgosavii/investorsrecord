from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


    path('add-investor/', add_investor, name='add_investor'),
    path('update-investor/<investor_id>', update_investor, name='update_investor'),
    path('delete-investor/<investor_id>', delete_investor, name='delete_investor'),
    path('list-investor/', list_investor, name='list_investor'),

    path('add-operator/', add_operator, name='add_operator'),
    path('update-operator/<operator_id>', update_operator, name='update_operator'),
    path('delete-operator/<operator_id>', delete_operator, name='delete_operator'),
    path('list-operator/', list_operator, name='list_operator'),

    path('add-transactions/', add_transactions, name='add_transactions'),
    path('update-transactions/<transactions_id>', update_transactions, name='update_transactions'),
    path('delete-transactions/<transactions_id>', delete_transactions, name='delete_transactions'),
    path('list-transactions/', list_transactions, name='list_transactions'),


    path('report/', report, name='report'),
    path('downlad-report/', report_download, name='report_download'),




] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)