import unittest
from unittest.mock import patch, AsyncMock
from app.binance import BinanceWSConsumer

class TestBinanceWSConsumer(unittest.IsolatedAsyncioTestCase):
    async def test_connect(self):
        consumer = BinanceWSConsumer()
        with patch('websockets.connect', new_callable=AsyncMock) as mock_connect:
            await consumer.connect("wss://test.websocket.url")
            mock_connect.assert_called_once_with("wss://test.websocket.url")
            self.assertIsNotNone(consumer.websocket)

    async def test_receive(self):
        consumer = BinanceWSConsumer()
        consumer.websocket = AsyncMock()
        consumer.websocket.recv = AsyncMock(return_value='{"c": "1000.0", "E": 1234567890}')
        price, timestamp = await consumer.receive()
        self.assertEqual(price, 1000.0)
        self.assertEqual(timestamp, 1234567890)

    async def test_disconnect(self):
        consumer = BinanceWSConsumer()
        with patch('websockets.connect', new_callable=AsyncMock):
            await consumer.connect("wss://test.websocket.url")
            await consumer.disconnect()
            self.assertIsNone(consumer.websocket)

    async def test_disconnect_without_connect(self):
        consumer = BinanceWSConsumer()
        await consumer.disconnect()  # Should not raise an exception
        self.assertIsNone(consumer.websocket)
