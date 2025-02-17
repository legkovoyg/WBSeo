# description/utils/cache_utils.py
from django.core.cache import cache
from hashlib import sha256

def generate_cache_key(sku_id, tone, language, exclude_keywords, include_keywords):
    """
    Генерирует уникальный ключ для кэша.
    Убираем слишком длинные строки, используя хеширование.

    :param sku_id:
    :param tone:
    :param language:
    :param exclude_keywords:
    :param include_keywords:
    :return:
    """

    key_data = f"{sku_id}_{tone}_{language}_{'_'.join(exclude_keywords)}__{'_'.join(include_keywords)}"
    return f"desc_{sha256(key_data.encode()).hexdigest()}"

def get_cached_description(cache_key):
    """
    Получает кэшированный результат

    :param cache_key:
    :return:
    """
    return cache.get(cache_key)

def set_cached_description(cache_key, result, timeout=300):
    """
    Сохраняет результат в кэше

    :param cache_key:
    :param result:
    :param timeout:
    :return:
    """
    cache.set(cache_key, result, timeout)
