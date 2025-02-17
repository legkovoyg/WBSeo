from django.test import TestCase
from description.utils.ai_utils import generate_prompt, request_to_openai
from unittest.mock import patch, MagicMock


class GeneratePromptTest(TestCase):
    """ Unittest - Тесты для функции generate_prompt """

    def setUp(self):
        """ Подготавливаем тестовые данные """
        self.wb_data = {
            "title": "Зимняя куртка Arctic Frost",
            "category": "Одежда",
            "material": "нейлон",
            "sizes": "42-56"
        }

        class MockRequestData:
            """ Имитация объекта сериализатора """
            validated_data = {
                "sku_id": "123456",
                "tone": "продающий",
                "language": "ru",
                "exclude_keywords": ["дешевый", "скидка"],
                "include_keywords": ["теплая", "зимняя"]
            }

        self.request_data = MockRequestData()

    def test_generate_prompt_success(self):
        """ Проверяем корректность формируемого промпта """
        expected_prompt = (
            'Напиши SEO-описание для товара "Зимняя куртка Arctic Frost".'
            'Категория: Одежда.'
            'Характеристики: нейлон, 42-56.'
            'Стиль: продающий.'
            'Язык: ru.'
            'Исключить слова: дешевый, скидка.'
            'Ключевые слова: теплая, зимняя.'
        )

        prompt = generate_prompt(self.wb_data, self.request_data)
        self.assertEqual(prompt, expected_prompt)

    def test_generate_prompt_with_missing_values(self):
        """ Проверяем поведение при отсутствии данных """
        wb_data_missing = {}  # Пустые данные Wildberries
        request_data_missing = type("MockRequest", (), {"validated_data": {}})()

class RequestToOpenAITest(TestCase):
    """ Unittest - Тестируем функцию request_to_openai """

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

    @patch("description.utils.ai_utils.openai.ChatCompletion.create")
    def test_request_to_openai_success(self, mock_openai):
        """ Проверяем успешный ответ OpenAI """
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Генерируемое SEO-описание"
        mock_openai.return_value = mock_response
        response = request_to_openai(self.prompt)
        self.assertEqual(response, "Генерируемое SEO-описание")
        mock_openai.assert_called_once()

    @patch("description.utils.ai_utils.openai.ChatCompletion.create")
    def test_request_to_openai_error(self, mock_openai):
        """ Проверяем обработку ошибки OpenAI """
        mock_openai.side_effect = Exception("API недоступно")
        with self.assertRaises(RuntimeError) as context:
            request_to_openai(self.prompt)
        self.assertIn("Ошибка запроса к OpenAI: API недоступно", str(context.exception))



