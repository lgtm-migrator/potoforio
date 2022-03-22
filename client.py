import time

import requests
from tabulate import tabulate
import os
import datetime


def cls():
    print('\n' * 10)


last_total = 0


def print_balances():
    global last_total
    wallets = requests.get('http://127.0.0.1:8000/api/wallet/').json()

    headers = ["Ticker", "Balance", "Price", "Value"]

    balances = {}
    prices = {}
    for wallet in wallets:

        assets_on_blockchains = wallet.get('assets_on_blockchains')
        for assets_on_blockchain in assets_on_blockchains:
            asset_on_blockchain = assets_on_blockchain.get('asset_on_blockchain')
            ticker = asset_on_blockchain.get('asset').get('ticker')
            last_price = asset_on_blockchain.get('asset').get('last_price')
            decimals = asset_on_blockchain.get('asset').get('decimals')
            balance = assets_on_blockchain.get('balance').get('balance')
            balance = int(balance) / pow(10, decimals)

            balances[ticker] = balances.get(ticker, 0) + balance
            prices[ticker] = last_price

    data = [(ticker, balance, prices[ticker], prices[ticker] * balance) for ticker, balance in balances.items()]

    print(tabulate(data, headers=headers))

    total_balance = sum([data[3] for data in data])

    balance_change = total_balance - last_total

    balance_change_str = f"{balance_change:.2f}"

    print(f"Total balance: {total_balance:.0f} ({'~' if not last_total else balance_change_str})")

    last_total = total_balance


while True:
    cls()
    print(f"Updated on: {datetime.datetime.now()}")
    print_balances()

    time.sleep(60*60)
