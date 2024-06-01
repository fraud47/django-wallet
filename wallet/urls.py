from django.urls import path
from .views import TransferAPIView, WalletBalanceAPIView, WalletListCreateAPIView, WalletDetailAPIView

urlpatterns = [
    path('api/wallets/', WalletListCreateAPIView.as_view(), name='wallet-list-create'),
    path('api/wallets/<int:pk>/', WalletDetailAPIView.as_view(), name='wallet-detail'),
    path('api/balance/', WalletBalanceAPIView.as_view(), name='wallet-balance'),
    path('api/transfer/', TransferAPIView.as_view(), name='wallet-transfer'),

]
