# description/utils/bd_utils.py
from description.models import Prompt, GeneratedDescription

def save_prompt_and_description(
    sku_id: str,
    tone: str,
    language: str,
    exclude_keywords: list,
    include_keywords: list,
    description: str
):
    """
    Сохраняет (или обновляет) Prompt и GeneratedDescription в базе данных.
    Возвращает кортеж (prompt_obj, generated_desc_obj).
    """
    # 1. Создаём (или получаем) Prompt
    prompt_obj, created = Prompt.objects.get_or_create(
        sku_id=sku_id,
        tone=tone,
        language=language,
        defaults={
            "exclude_keywords": exclude_keywords,
            "include_keywords": include_keywords,
        }
    )
    # Если Prompt уже существует, при необходимости обновляем поля
    if not created:
        prompt_obj.exclude_keywords = exclude_keywords
        prompt_obj.include_keywords = include_keywords
        prompt_obj.save()

    # 2. Создаём (или обновляем) GeneratedDescription
    generated_desc_obj, _ = GeneratedDescription.objects.update_or_create(
        prompt=prompt_obj,
        defaults={
            "description": description
        }
    )

    return prompt_obj, generated_desc_obj
