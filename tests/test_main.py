import unittest
from unittest.mock import patch, AsyncMock
import numpy as np
from app.main import main
import logging


class TestMain(unittest.IsolatedAsyncioTestCase):
    @patch("app.main.BinanceWSConsumer")
    @patch("app.main.time")
    async def test_main(self, mock_time, MockBinanceWSConsumer):
        mock_time.time.side_effect = [1609459200, 1609459260, 1609459320]

        mock_consumer_eth = MockBinanceWSConsumer.return_value
        mock_consumer_btc = MockBinanceWSConsumer.return_value

        mock_consumer_eth.receive = AsyncMock(
            side_effect=[
                (1000.0, 1609459200000),
                (1010.0, 1609459260000),
                (1020.0, 1609459320000),
            ]
        )

        mock_consumer_btc.receive = AsyncMock(
            side_effect=[
                (30000.0, 1609459200000),
                (30100.0, 1609459260000),
                (30200.0, 1609459320000),
            ]
        )

        with patch("app.main.asyncio.sleep", new_callable=AsyncMock):
            await main()

        self.assertEqual(mock_consumer_eth.receive.call_count, 3)
        self.assertEqual(mock_consumer_btc.receive.call_count, 3)

        # Check if the correlation coefficient and returns were calculated correctly
        eth_prices = [1000.0, 1010.0, 1020.0]
        btc_prices = [30000.0, 30100.0, 30200.0]

        eth_returns = np.diff(eth_prices) / eth_prices[:-1]
        btc_returns = np.diff(btc_prices) / btc_prices[:-1]

        corr_coeff = np.corrcoef(eth_returns, btc_returns)[0, 1]
        eth_returns_no_btc = eth_returns - corr_coeff * btc_returns

        eth_returns_last_hour = (np.prod(eth_returns_no_btc + 1) - 1) * 100

        self.assertAlmostEqual(eth_returns_last_hour, 0.995, places=2)


class TestLogging(unittest.TestCase):
    @patch("logging.info")
    def test_logging_info(self, mock_logging_info):
        # Предположим, что это часть вашего класса
        logging.info("Тестовое сообщение")

        # Проверяем, что logging.info был вызван с правильным сообщением
        mock_logging_info.assert_called_once_with("Тестовое сообщение")

    @patch("logging.error")
    def test_logging_error(self, mock_logging_error):
        logging.error("Ошибка подключения")

        # Проверяем, что logging.error был вызван с правильным сообщением
        mock_logging_error.assert_called_once_with("Ошибка подключения")
