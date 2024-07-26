import logging

def setup_logging():
    """
    Configura o logging para salvar logs em um arquivo chamado 'app.log'.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
        ]
    )
