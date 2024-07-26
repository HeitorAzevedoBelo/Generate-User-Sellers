import unittest
from unittest.mock import patch, AsyncMock
import main
from argparse import Namespace

class TestMain(unittest.TestCase):

    @patch('main.asyncio.run')
    @patch('main.async_main', new_callable=AsyncMock)
    def test_main_generate_mongo(self, mock_async_main, mock_asyncio_run):
        args = Namespace(generate=10, output='mongo', connection='mongodb://localhost:27017', filename=None)
        with patch('main.config', new={"MONGO_DATABASE": "test_db", "MONGO_COLLECTION": "test_collection"}):
            main.run_main(args)
            mock_asyncio_run.assert_called_once()
            mock_async_main.assert_called_once_with(args, main.config)

    @patch('main.sync_main')
    def test_main_generate_json(self, mock_sync_main):
        args = Namespace(generate=10, output='json', connection=None, filename=None)
        with patch('main.config', new={"MONGO_DATABASE": "test_db", "MONGO_COLLECTION": "test_collection"}):
            main.run_main(args)
            mock_sync_main.assert_called_once_with(args, main.config)

if __name__ == "__main__":
    unittest.main()
