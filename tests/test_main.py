import unittest
import asyncio
from unittest.mock import patch, AsyncMock
from app.main import main, BinanceWSConsumer


class TestMain(unittest.TestCase):

    @patch('app.main.BinanceWSConsumer.connect', new_callable=AsyncMock)
    @patch('app.main.BinanceWSConsumer.receive', new_callable=AsyncMock)
    @patch('app.main.BinanceWSConsumer.disconnect', new_callable=AsyncMock)
    @patch('numpy.corrcoef', return_value=[[1, 0.5], [0.5, 1]])
    @patch('numpy.prod', return_value=1.02)
    def test_main(self, mock_prod, mock_corrcoef, mock_disconnect, mock_receive, mock_connect):
        mock_receive.side_effect = [
            (2000.0, 1234567890000),  # ETH price, timestamp
            (60000.0, 1234567890000),  # BTC price, timestamp
            (2000.1, 1234567890100),
            (60000.1, 1234567890100)
        ]

        asyncio.run(main())

        self.assertTrue(mock_connect.called)
        self.assertTrue(mock_receive.called)
        self.assertTrue(mock_disconnect.called)


if __name__ == '__main__':
    unittest.main()
