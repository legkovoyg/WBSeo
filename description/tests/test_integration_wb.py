from django.test import TestCase
from description.utils.wb_utils import get_sku_data
import os

class WildberriesIntegrationTest(TestCase):
    """ Интеграционный тест для get_sku_data с реальным запросом к Wildberries API """

    def setUp(self):
        """ Устанавливаем тестовые данные """
        self.valid_sku = "165682647"
        self.invalid_sku = "000000000"

    def test_get_sku_data_success(self):
        """ Проверяем, что запрос к Wildberries API проходит успешно и возвращает JSON """
        response = get_sku_data(self.valid_sku)
        print(response)
        self.assertIsInstance(response, dict)  # Ответ должен быть JSON (dict)
        self.assertIn("data", response)  # Ожидаем ключ "data"
        self.assertIn("products", response["data"])  # Внутри "data" должен быть список "products"
        self.assertGreater(len(response["data"]["products"]), 0)  # В списке должен быть хотя бы 1 товар

    def test_get_sku_data_not_found(self):
        """
        Проверяем, что при запросе несуществующего SKU выбрасывается ValueError,
        потому что products пустой.
        """
        with self.assertRaises(ValueError) as context:
            get_sku_data(self.invalid_sku)
        self.assertIn("не найден в Wildberries (пустые products)", str(context.exception))

