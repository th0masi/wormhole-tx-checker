import random

from core.utils import load_from_file, write_success_wallet
import requests
from loguru import logger
from pyuseragents import random as random_useragent
import uuid


def check_stat_by_wallet(address):
    stat = Stats(wallet=address)
    result = stat.get_stat_by_wallet()

    if result:
        write_success_wallet(
            file_path='data/success_wallets.txt',
            wallet=address,
        )


def check_stats(wallets_data):
    for wallet in wallets_data:
        check_stat_by_wallet(address=wallet)

    logger.info(f'Получил данные для всех кошельков')


class Stats:
    def __init__(self, wallet):
        self.proxy_list = load_from_file("data/proxies.txt")
        self.wallet = wallet
        self.attempts = 3
        self.url = (f'https://api.wormholescan.io/api/v1/transactions?'
                    f'address={self.wallet}'
                    f'&page=0&pageSize=10&sortOrder=ASC')

    def get_stat_by_wallet(self):
        response = self.send_request(self.url)
        try:
            data = response.json()
            if 'transactions' in data and isinstance(data['transactions'], list):
                num_transactions = len(data['transactions'])
                if num_transactions > 0:
                    logger.success(f"{self.wallet} | {num_transactions} транзакций")
                    return True
                else:
                    logger.warning(f"{self.wallet} | нет транзакций")
            else:
                logger.warning(f"{self.wallet} | нет транзакций")
        except ValueError:
            logger.error("Ошибка при десериализации JSON")
        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e}")

        return False

    def send_request(self, url):
        headers = self.get_headers()

        random.shuffle(self.proxy_list)

        for proxy in self.proxy_list:
            try:
                proxy = {
                    "http"  : f"http://{proxy}",
                    "https" : f"http://{proxy}"
                }

                response = requests.get(
                    url=url,
                    headers=headers,
                    proxies=proxy
                )

                return response

            except Exception:
                continue

    @staticmethod
    def get_headers():
        base_headers = {
            "Content-Type"  : 'application/json',
            "User-Agent"    : random_useragent(),
            "origin"        : 'https://wormholescan.io',
            "referer"       : f'https://wormholescan.io/',
        }

        return base_headers

