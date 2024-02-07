from core.checker import check_stats
from core.logger_config import setup_logger
from core.utils import load_from_file


if __name__ == '__main__':
    setup_logger()

    wallets_list = load_from_file("data/wallets.txt")
    check_stats(wallets_list)
