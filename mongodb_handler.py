import motor.motor_asyncio
import logging

class MongoDBHandler:
    def __init__(self, connection_str: str, database: str, collection: str):
        """
        Inicializa a classe MongoDBHandler com as configurações fornecidas.

        Parâmetros:
        connection_str (str): String de conexão para o MongoDB.
        database (str): Nome do banco de dados.
        collection (str): Nome da coleção.
        """
        self.connection_str = connection_str
        self.database = database
        self.collection = collection
        self.client = None
        self.db = None
        self.coll = None

    async def connect(self):
        """
        Conecta ao MongoDB usando a string de conexão fornecida.

        Lança:
        ConnectionError: Se a conexão ao MongoDB falhar.
        """
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(self.connection_str)
            self.db = self.client[self.database]
            self.coll = self.db[self.collection]
            logging.info("Connected to MongoDB.")
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            raise

    async def insert_many(self, data: list):
        """
        Insere múltiplos documentos na coleção MongoDB.

        Parâmetros:
        data (list): Lista de dicionários a serem inseridos.

        Lança:
        PyMongoError: Se a inserção de dados falhar.
        """
        try:
            await self.coll.insert_many(data)
            logging.info("Data successfully inserted into MongoDB.")
        except Exception as e:
            logging.error(f"Error inserting data into MongoDB: {e}")
            raise
