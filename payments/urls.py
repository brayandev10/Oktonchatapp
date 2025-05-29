from django.urls import path
from . import views

urlpatterns = [
    path('', views.paiement, name='paiement'),
    path('pay/', views.paiement_cinetpay, name='paiement_cinetpay'),
    path('notification/', views.cinetpay_notification, name='cinetpay_notification'),
    path('succes/', views.paiement_succes, name='paiement_succes'),
]