from django.urls import path
from core import views

urlpatterns = [
    path('blockchain/', views.BlockchainListCreateAPIView.as_view()),
    path('asset/', views.AssetListCreateAPIView.as_view()),
    path('wallet/', views.WalletListCreateAPIView.as_view()),
    path('history/', views.BalanceHistoryListAPIView.as_view()),
    path('wallet/<pk>', views.WalletRetrieveUpdateDestroyAPIView.as_view()),

    path('asset_on_blockchain/', views.AssetOnBlockchainListCreateAPIView.as_view()),

]
