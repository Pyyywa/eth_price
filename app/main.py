import asyncio
import numpy as np
import time
import logging
from app.binance import BinanceWSConsumer

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

TIME = 3600000  # 1 час в миллисекундах


async def main():
    eth_prices = []
    btc_prices = []
    bwsc1 = BinanceWSConsumer()
    bwsc2 = BinanceWSConsumer()

    await asyncio.gather(
        bwsc1.connect("wss://fstream.binance.com/ws/ethusdt@ticker"),
        bwsc2.connect("wss://fstream.binance.com/ws/btcusdt@ticker"),
    )

    try:
        while True:
            eth_price, eth_timestamp = await bwsc1.receive()
            btc_price, btc_timestamp = await bwsc2.receive()

            if eth_price is not None and btc_price is not None:
                eth_prices.append([eth_price, eth_timestamp])
                btc_prices.append([btc_price, btc_timestamp])
                logger.info(
                    f"ETHUSDT PRICE: {eth_price}, "
                    f"ETH TIMESTAMP: {eth_timestamp}, "
                    f"BTCUSDT PRICE: {btc_price}, "
                    f"BTC TIMESTAMP: {btc_timestamp}"
                )

            current_time = round(time.time() * 1000)


            if current_time - eth_prices[0][1] > TIME:
                eth_prices_np = np.array(eth_prices)
                btc_prices_np = np.array(btc_prices)

                if len(eth_prices_np) < 2 or len(btc_prices_np) < 2:
                    continue

                eth_returns = np.diff(eth_prices_np[:, 0]) / eth_prices_np[:-1, 0]
                btc_returns = np.diff(btc_prices_np[:, 0]) / btc_prices_np[:-1, 0]

                if np.any(btc_prices_np[:-1, 0] == 0):
                    logger.warning("Обнаружено деление на ноль в расчетах.")
                    continue

                corr_coeff = np.corrcoef(eth_returns, btc_returns)[0, 1]
                eth_returns_no_btc = eth_returns - corr_coeff * btc_returns

                eth_returns_last_hour = (np.prod(eth_returns_no_btc + 1) - 1) * 100
                logger.info(f"Course change: {eth_returns_last_hour:.2f}%")

                # Удаляем старые данные
                del eth_prices[0]
                del btc_prices[0]

                # Выводим результат, если колебание превышает 1%
                if abs(eth_returns_last_hour) > 1:
                    print(
                        f"Колебание ETH "
                        f"{round(eth_returns_last_hour, 2)}% за прошедший час!"
                    )

            await asyncio.sleep(0.1)
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
    finally:
        await bwsc1.disconnect()
        await bwsc2.disconnect()


# Запуск основного цикла
if __name__ == "__main__":
    asyncio.run(main())
