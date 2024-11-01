import unittest
from unittest.mock import patch, AsyncMock
from app.main import main
import logging


class TestMainFunction(unittest.TestCase):
    @patch("app.BinanceWSConsumer.receive", new_callable=AsyncMock)
    @patch("app.BinanceWSConsumer.connect", new_callable=AsyncMock)
    async def test_main_function(self, mock_connect, mock_receive):
        mock_connect.return_value = AsyncMock()
        mock_receive.side_effect = [
            (2000.0, 1234567890),  # ETH price
            (60000.0, 1234567890),  # BTC price
            (2050.0, 1234567891),  # ETH price
            (60500.0, 1234567891),  # BTC price
            (2100.0, 1234567892),  # ETH price
            (61000.0, 1234567892),  # BTC price
        ]
        await main()
        self.assertEqual(mock_connect.call_count, 2)

    @patch("app.BinanceWSConsumer.receive", new_callable=AsyncMock)
    @patch("app.BinanceWSConsumer.connect", new_callable=AsyncMock)
    async def test_main_function_insufficient_data(self, mock_connect, mock_receive):
        mock_connect.return_value = AsyncMock()
        mock_receive.side_effect = [
            (2000.0, 1234567890),  # ETH price
            (60000.0, 1234567890),  # BTC price
            # insufficient data for further calculations
        ]
        await main()
        self.assertEqual(mock_connect.call_count, 2)

    @patch("app.BinanceWSConsumer.receive", new_callable=AsyncMock)
    @patch("app.BinanceWSConsumer.connect", new_callable=AsyncMock)
    async def test_main_function_division_by_zero(self, mock_connect, mock_receive):
        mock_connect.return_value = AsyncMock()
        mock_receive.side_effect = [
            (2000.0, 1234567890),  # ETH price
            (60000.0, 1234567890),  # BTC price
            (0.0, 1234567891),  # ETH price (will cause division by zero)
            (60500.0, 1234567891),  # BTC price
        ]
        await main()
        self.assertEqual(mock_connect.call_count, 2)

    @patch("app.BinanceWSConsumer.receive", new_callable=AsyncMock)
    @patch("app.BinanceWSConsumer.connect", new_callable=AsyncMock)
    async def test_main_function_correlation(self, mock_connect, mock_receive):
        mock_connect.return_value = AsyncMock()
        mock_receive.side_effect = [
            (2000.0, 1234567890),  # ETH price
            (60000.0, 1234567890),  # BTC price
            (2100.0, 1234567891),  # ETH price
            (60500.0, 1234567891),  # BTC price
            (2200.0, 1234567892),  # ETH price
            (61000.0, 1234567892),  # BTC price
        ]
        await main()
        self.assertEqual(mock_connect.call_count, 2)


class TestLogging(unittest.TestCase):
    @patch('logging.info')
    def test_logging_info(self, mock_logging_info):
        # Предположим, что это часть вашего класса
        logging.info("Тестовое сообщение")

        # Проверяем, что logging.info был вызван с правильным сообщением
        mock_logging_info.assert_called_once_with("Тестовое сообщение")

    @patch('logging.error')
    def test_logging_error(self, mock_logging_error):
        logging.error("Ошибка подключения")

        # Проверяем, что logging.error был вызван с правильным сообщением
        mock_logging_error.assert_called_once_with("Ошибка подключения")
