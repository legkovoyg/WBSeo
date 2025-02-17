import openai
from django.conf import settings


def generate_prompt(wb_data, request_data) -> str:
    """
    Создаем промпт

    :param wb_data:
    :param request_data:
    :return: prompt
    """
    # wb_data
    brand = (
        wb_data
        .get("data", {})
        .get("products", [{}])[0]
        .get("brand", "неизвестно")
    )
    product_name = (
        wb_data
        .get("data", {})
        .get("products", [{}])[0]
        .get("name", "не указано")
    )
    product_entity = (
        wb_data
        .get("data", {})
        .get("products", [{}])[0]
        .get("entity", "не указано")
    )

    # request_data
    sku_id = request_data.validated_data.get("sku_id")
    tone = request_data.validated_data.get("tone")
    language = request_data.validated_data.get("language")
    exclude_keywords = request_data.validated_data.get("exclude_keywords")
    include_keywords = request_data.validated_data.get("include_keywords")

    prompt = (
        f'Напиши SEO-описание для товара "{product_name}".\n'
        f'Категория: {product_entity}.\n'
        f'Бренд: {brand}.\n'
        f'Стиль: {tone}.\n'
        f'Язык: Русский.\n'
        f'Исключить слова: {", ".join(exclude_keywords) if exclude_keywords else "нет"}.\n'
        f'Ключевые слова: {", ".join(include_keywords) if include_keywords else "не указаны"}.\n'
    )
    return prompt

def request_to_openai(prompt: str) -> str:
    """
    Делает запрос к OpenAI, или вызывает ошибку
    :param prompt:
    :return:
    """
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            timeout=20
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Ошибка запроса к OpenAI: {str(e)}")

