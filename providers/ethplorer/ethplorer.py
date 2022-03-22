import aiohttp
from providers import BalanceProvider

from core.models import Wallet, Blockchain, AssetOnBlockchain


class EthplorerClient(BalanceProvider):
    API_URL = 'https://api.ethplorer.io'

    def __init__(self, apikey="freekey"):
        super().__init__()
        self._api_key = apikey

    async def scan_wallet(self, wallet: Wallet):
        params = {
            'apiKey': self._api_key
        }
        url = f"{EthplorerClient.API_URL}/getAddressInfo/{wallet.address}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response = await response.json()

                blockchain_eth = Blockchain.objects.filter(name="Ethereum").last()
                eth_on_eth = AssetOnBlockchain.objects.filter(blockchain=blockchain_eth, asset__ticker="ETH").last()
                eth_balance = response.get('ETH').get('rawBalance')

                await self._update_balance(
                    wallet=wallet,
                    blockchain=blockchain_eth,
                    asset=eth_on_eth.asset,
                    balance=eth_balance
                )

                assets = response.get('tokens', [])
                for asset in assets:
                    address = asset.get('tokenInfo').get('address')
                    balance = asset.get("rawBalance")
                    ticker = "<UNKNOWN>"

                    asset_on_eth = AssetOnBlockchain.objects.filter(blockchain=blockchain_eth, address=address).last()
                    if not asset_on_eth:
                        self._logger.warning(f"Unknown asset: {balance} {ticker} with address {address}")
                        continue

                    await self._update_balance(
                        wallet=wallet,
                        blockchain=blockchain_eth,
                        asset=asset_on_eth.asset,
                        balance=balance
                    )

    def match_address(self, address: str):
        return len(address) == 42 and address.startswith('0x')
