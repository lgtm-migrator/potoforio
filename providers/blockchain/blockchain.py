from providers import BalanceProvider

from core.models import Wallet, Blockchain, AssetOnBlockchain


class BlockchainClient(BalanceProvider):
    API_URL = 'https://blockchain.info'

    async def scan_wallet(self, wallet: Wallet):
        url = f"{BlockchainClient.API_URL}/balance?active={wallet.address}"
        response = await self._request('GET', url)
        response = await response.json()

        blockchain_btc = Blockchain.objects.filter(name="Bitcoin").last()
        btc_on_btc = AssetOnBlockchain.objects.filter(blockchain=blockchain_btc, asset__ticker="BTC").last()

        balance = str(response.get(wallet.address).get('final_balance'))

        await self._update_balance(
            wallet=wallet,
            blockchain=blockchain_btc,
            asset=btc_on_btc.asset,
            balance=balance
        )

    def match_address(self, address: str):
        return len(address) == 34 and address.startswith('3')
