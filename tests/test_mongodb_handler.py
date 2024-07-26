import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from mongodb_handler import MongoDBHandler

class TestMongoDBHandler(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.handler = MongoDBHandler("mongodb://localhost:27017", "test_db", "test_collection")

    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    async def test_connect(self, mock_client):
        mock_client.return_value = AsyncMock()
        await self.handler.connect()
        mock_client.assert_called_with("mongodb://localhost:27017")

    @patch('motor.motor_asyncio.AsyncIOMotorClient')
    async def test_insert_many(self, mock_client):
        mock_coll = AsyncMock()
        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_coll
        mock_client.return_value.__getitem__.return_value = mock_db

        await self.handler.connect()
        data = [{"test": "data"}]
        await self.handler.insert_many(data)
        mock_coll.insert_many.assert_awaited_once_with(data)

if __name__ == "__main__":
    unittest.main()
