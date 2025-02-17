from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.conf import settings

from description.serializers import GenerateDescriptionSerializer

#utils
import description.utils.wb_utils as wb_utils
import description.utils.ai_utils as ai_utils
import description.utils.common_utils as common_utils
import description.utils.cache_utils as cache_utils
import description.utils.bd_utils as bd_utils



class GenerateDescriptionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GenerateDescriptionSerializer(data=request.data)
        if serializer.is_valid():
            sku_id = serializer.validated_data.get("sku_id")
            tone = serializer.validated_data.get("tone")
            language = serializer.validated_data.get("language")
            exclude_keywords = serializer.validated_data.get("exclude_keywords")
            include_keywords = serializer.validated_data.get("include_keywords")

            # Генерируем ключ для кэша (оптимизированный)
            cache_key = cache_utils.generate_cache_key(sku_id, tone, language, exclude_keywords, include_keywords)

            # Проверяем, есть ли данные в кэше
            cached_result = cache_utils.get_cached_description(cache_key)
            if cached_result:
                return Response(cached_result, status=status.HTTP_200_OK)

            # 1. Получаем данные о товаре с Wildberries API
            try:
                sku_data = wb_utils.get_sku_data(sku_id)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except ConnectionError as e:
                return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 2. Формируем промпт для GPT-4o
            prompt = ai_utils.generate_prompt(sku_data, serializer)

            # 3. Запрос к GPT-4o
            try:
                description = ai_utils.request_to_openai(prompt)
            except RuntimeError as e:
                return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 4. Проверка уникальности
            unique_score = common_utils.check_uniqueness(description)
            result = {
                "description": description,
                "unique_score": unique_score
            }
            # 5. Сейв в БД
            bd_utils.save_prompt_and_description(
                sku_id=sku_id,
                tone=tone,
                language=language,
                exclude_keywords=exclude_keywords,
                include_keywords=include_keywords,
                description=description
            )

            # 6. Кэшируем результат
            cache.set(cache_key, result, timeout=300)

            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
