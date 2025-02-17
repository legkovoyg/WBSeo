import requests
from django.conf import settings

import requests

import requests

def get_sku_data(sku_id: str) -> dict:
    """
    Получает данные о товаре с публичного эндпоинта Wildberries по SKU.
    Возвращает JSON или выбрасывает исключение при ошибке.
    """
    WB_API_URL = "https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm="
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(f"{WB_API_URL}{sku_id}", headers=headers, timeout=10)
        response.raise_for_status()  # выбросит ошибку, только если статус != 200..399

        data = response.json()
        # Если products пуст, считаем, что SKU не найден
        if not data["data"]["products"]:
            raise ValueError(f"SKU {sku_id} не найден в Wildberries (пустые products).")

        return data
    except requests.exceptions.HTTPError as e:
        raise ValueError(f"Ошибка Wildberries API: {response.status_code} {response.text}") from e
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка сети при запросе к Wildberries API: {str(e)}") from e

