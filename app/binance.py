import websockets
import json
import time
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class BinanceWSConsumer:
    def __init__(self):
        self.websocket = None

    async def connect(self, url):
        """Устанавливает соединение с WebSocket."""
        try:
            self.websocket = await websockets.connect(url)
            logging.info("Успешно подключено к WebSocket")
        except Exception as e:
            logging.error(f"Ошибка подключения к WebSocket: {e}")

    async def receive(self):
        """Получает данные из WebSocket."""
        if self.websocket is None:
            logging.warning("WebSocket не подключен. Вызовите connect сначала")
            raise RuntimeError("WebSocket not connected. Call connect first")

        try:
            data = json.loads(await self.websocket.recv())
            price = data["c"]
            timestamp = data.get("E", time.time())
            return float(price), timestamp
        except json.JSONDecodeError:
            logging.error("Ошибка декодирования JSON")
            return None, None
        except Exception as e:
            logging.error(f"Ошибка при получении данных: {e}")
            return None, None

    async def disconnect(self):
        """Закрывает соединение с WebSocket."""
        if self.websocket is not None:
            await self.websocket.close()
            logging.info("Соединение с WebSocket закрыто")
            self.websocket = None
