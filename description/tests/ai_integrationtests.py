import time
from django.test import TestCase
from description.utils.ai_utils import request_to_openai

class RequestToOpenAIIntegrationTest(TestCase):
    """ Интеграционный тест для OpenAI """

    def setUp(self):
        """ Подготавливаем тестовые данные """
        self.prompt = (
            'Напиши SEO-описание для товара "Зимняя куртка Arctic Frost".'
            'Категория: Одежда.'
            'Характеристики: нейлон, 42-56.'
            'Стиль: продающий.'
            'Язык: ru.'
            'Исключить слова: дешевый, скидка.'
            'Ключевые слова: теплая, зимняя.'
        )

    def test_openai_integration(self):
        """ Проверяем, что запрос к OpenAI возвращает текст """
        print(f'Был отправлен prompt: {self.prompt}')
        response = request_to_openai(self.prompt)
        print(f'Получен ответ response: {response}')
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
