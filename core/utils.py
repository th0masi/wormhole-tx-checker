import os

from loguru import logger


def load_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        logger.error(f"Ошибка: файл не найден – {file_path}")
        exit()


def write_success_wallet(
        file_path: str,
        wallet: str
) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "a") as file:
        file.write(wallet + "\n")
