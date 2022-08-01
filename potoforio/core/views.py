import datetime
import pytz

from rest_framework import filters, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Blockchain, Asset, Wallet, AssetOnBlockchain, BalanceHistory, Provider, NFT
from .serializers import BlockchainSerializer, AssetSerializer, WalletSerializer, \
    AssetOnBlockchainSerializer, BalanceHistorySerializer, ProviderSerializer, NFTSerializer
from .paginations import NFTPageNumberPagination


class BlockchainListCreateAPIView(generics.ListCreateAPIView):
    queryset = Blockchain.objects.all()
    serializer_class = BlockchainSerializer


class AssetListCreateAPIView(generics.ListCreateAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class WalletListCreateAPIView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class AssetOnBlockchainListCreateAPIView(generics.ListCreateAPIView):
    queryset = AssetOnBlockchain.objects.all()
    serializer_class = AssetOnBlockchainSerializer


class BalanceHistoryListAPIView(generics.ListAPIView):
    serializer_class = BalanceHistorySerializer

    def get_queryset(self):
        """
        Filtering
        """
        start_timestamp = self.request.GET.get('start_timestamp', 0)
        start_timestamp = self._parse_start_timestamp(start_timestamp)

        return BalanceHistory.objects.filter(timestamp__gte=start_timestamp)

    @staticmethod
    def _parse_start_timestamp(start_timestamp):
        """
        convert start_timestamp to datetime or raise exception
        """
        # convert to datetime
        try:
            start_timestamp = int(start_timestamp) // 1000
            return datetime.datetime.fromtimestamp(start_timestamp, tz=pytz.UTC)
        except Exception:
            raise ValidationError(f'Can not parse {start_timestamp} as timestamp string')

    def list(self, request, *args, **kwargs):
        """
        Process data with custom format
        """
        data = [
             [int(item.timestamp.timestamp() * 1000), item.balance] for item in self.get_queryset()
        ]

        return Response(data)


class ProviderListAPIView(generics.ListAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class NFTListAPIView(generics.ListAPIView):
    queryset = NFT.objects.all()
    serializer_class = NFTSerializer
    pagination_class = NFTPageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'token_id', 'blockchain__name']
