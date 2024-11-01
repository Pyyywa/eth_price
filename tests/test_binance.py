import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import json
import logging
from app.binance import BinanceWSConsumer


class TestBinanceWSConsumer(unittest.TestCase):

    @patch("websockets.connect", new_callable=AsyncMock)
    async def asyncSetUp(self, mock_connect):
        """Фикстура для установки соединения с WebSocket."""
        self.consumer = BinanceWSConsumer()
        self.mock_connect = mock_connect
        await self.consumer.connect("wss://example.com")

    @patch("websockets.connect", new_callable=AsyncMock)
    async def test_connect_success(self, mock_connect):
        """Тест успешного подключения к WebSocket."""
        await self.asyncSetUp(mock_connect)
        self.assertIsNotNone(self.consumer.websocket)
        logging.info("Тест успешного подключения прошел.")

    @patch("websockets.connect", new_callable=AsyncMock)
    async def test_connect_failure(self, mock_connect):
        """Тест обработки ошибки подключения к WebSocket."""
        mock_connect.side_effect = Exception("Connection failed")
        await self.consumer.connect("wss://example.com")
        self.assertIsNone(self.consumer.websocket)
        logging.info("Тест неудачного подключения прошел.")

    @patch("websockets.connect", new_callable=AsyncMock)
    async def test_receive_success(self, mock_connect):
        """Тест успешного получения данных из WebSocket."""
        await self.asyncSetUp(mock_connect)
        self.consumer.websocket.recv = AsyncMock(
            return_value=json.dumps({"c": "100.0", "E": 1234567890})
        )

        price, timestamp = await self.consumer.receive()
        self.assertEqual(price, 100.0)
        self.assertEqual(timestamp, 1234567890)
        logging.info("Тест успешного получения данных прошел.")

    @patch("websockets.connect", new_callable=AsyncMock)
    async def test_receive_json_decode_error(self, mock_connect):
        """Тест обработки ошибки декодирования JSON."""
        await self.asyncSetUp(mock_connect)
        self.consumer.websocket.recv = AsyncMock(return_value="invalid json")

        price, timestamp = await self.consumer.receive()
        self.assertIsNone(price)
        self.assertIsNone(timestamp)
        logging.info("Тест обработки ошибки декодирования JSON прошел.")

    @patch("websockets.connect", new_callable=AsyncMock)
    async def test_receive_websocket_not_connected(self, mock_connect):
        """Тест обработки попытки получения данных при отключенном WebSocket."""
        with self.assertRaises(RuntimeError) as context:
            await self.consumer.receive()
        self.assertEqual(
            str(context.exception), "WebSocket not connected. Call connect() first."
        )
        logging.info(
            "Тест обработки попытки получения данных при отключенном WebSocket прошел."
        )

    @patch("websockets.connect", new_callable=AsyncMock)
    async def test_receive_general_error(self, mock_connect):
        """Тест обработки общей ошибки получения данных."""
        await self.asyncSetUp(mock_connect)
        self.consumer.websocket.recv = AsyncMock(side_effect=Exception("General error"))

        price, timestamp = await self.consumer.receive()
        self.assertIsNone(price)
        self.assertIsNone(timestamp)
        logging.info("Тест обработки общей ошибки получения данных прошел.")

    @patch("websockets.connect", new_callable=AsyncMock)
    async def test_disconnect_success(self, mock_connect):
        """Тест успешного отключения от WebSocket."""
        await self.asyncSetUp(mock_connect)
        await self.consumer.disconnect()
        self.assertIsNone(self.consumer.websocket)
        logging.info("Тест успешного отключения прошел.")

    @patch("websockets.connect", new_callable=AsyncMock)
    async def test_disconnect_when_not_connected(self, mock_connect):
        """Тест отключения при отсутствии подключения."""
        await self.consumer.disconnect()  # Должно пройти без ошибок
        logging.info("Тест отключения при отсутствии подключения прошел.")
