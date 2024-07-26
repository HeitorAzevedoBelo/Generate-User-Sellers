import json
import logging
import argparse
import asyncio
from time import sleep
from os import system, name, makedirs
from os.path import exists, join
from tqdm import tqdm
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
from data_generator import DataGenerator
from mongodb_handler import MongoDBHandler
from logger import setup_logging

# Configuração de logging
setup_logging()

# Inicializa o colorama
init(autoreset=True)

# Configuração global
config = None

# Funções utilitárias

def clear_screen():
    """
    Limpa a tela do terminal.
    """
    system('cls' if name == 'nt' else 'clear')

def cls_message(message, delay=2):
    """
    Exibe uma mensagem e limpa a tela após um atraso.
    
    Parâmetros:
    message (str): A mensagem a ser exibida.
    delay (int): O tempo em segundos antes de limpar a tela.
    """
    clear_screen()
    print(message)
    sleep(delay)
    clear_screen()

def print_main_menu():
    """
    Exibe o menu principal.
    """
    clear_screen()
    print(Fore.CYAN + "===============================")
    print(Fore.CYAN + "       Gerador de Dados        ")
    print(Fore.CYAN + "===============================")
    print(Fore.CYAN + "[1] Gerar documentos")
    print(Fore.CYAN + "[2] Sair")
    print(Fore.CYAN + "===============================")

def print_generation_menu():
    """
    Exibe o menu de opções de geração de dados.
    """
    clear_screen()
    print(Fore.CYAN + "===============================")
    print(Fore.CYAN + "    Opções de Geração de Dados ")
    print(Fore.CYAN + "===============================")
    print(Fore.CYAN + "[1] Salvar no MongoDB")
    print(Fore.CYAN + "[2] Salvar em um arquivo JSON")
    print(Fore.CYAN + "===============================")

def generate_users_parallel(data_generator, docs_count):
    """
    Gera usuários em paralelo.

    Parâmetros:
    data_generator (DataGenerator): Instância do gerador de dados.
    docs_count (int): Número de usuários a serem gerados.

    Retorno:
    list: Lista de usuários gerados.
    """
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(data_generator.generate_user) for _ in range(docs_count)]
        return [future.result() for future in tqdm(as_completed(futures), total=docs_count, desc="Gerando Usuários")]

async def async_main(args, config):
    """
    Função principal assíncrona para operações com MongoDB.

    Parâmetros:
    args: Argumentos da linha de comando.
    config: Configurações carregadas do arquivo config.json.
    """
    data_generator = DataGenerator(config)
    docs_count = args.generate

    if args.output == 'mongo':
        # Gera e salva os dados no MongoDB
        try:
            logging.info('Generating data and saving to MongoDB')
            connection_str = args.connection
            mongo_handler = MongoDBHandler(connection_str, config["MONGO_DATABASE"], config["MONGO_COLLECTION"])
            await mongo_handler.connect()
            
            users = generate_users_parallel(data_generator, docs_count)
            await mongo_handler.insert_many(users)
            sleep(1)
            cls_message(Fore.GREEN + 'Dados inseridos com sucesso!', delay=2)
        except Exception as e:
            logging.error(f"Error: {e}")
            cls_message(Fore.RED + f"Erro: {e}", delay=3)

def sync_main(args, config):
    """
    Função principal síncrona para operações não MongoDB.

    Parâmetros:
    args: Argumentos da linha de comando.
    config: Configurações carregadas do arquivo config.json.
    """
    data_generator = DataGenerator(config)
    docs_count = args.generate

    if args.output == 'json':
        # Gera e salva os dados em um arquivo JSON
        try:
            logging.info('Generating data and saving to JSON file')
            users = generate_users_parallel(data_generator, docs_count)
            directory = "output_json"
            if not exists(directory):
                makedirs(directory)
            file_name = args.filename if args.filename else 'dados.json'
            file_path = join(directory, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=4, default=data_generator.json_serial)
            cls_message(Fore.GREEN + f'Dados salvos com sucesso em {file_path}!', delay=2)
        except Exception as e:
            logging.error(f"Error saving to JSON file: {e}")
            cls_message(Fore.RED + f'Erro ao salvar o arquivo JSON: {e}', delay=3)

def run_main(args=None):
    """
    Função principal para o menu interativo ou execução com argumentos.
    """
    global config

    if args is None:
        parser = argparse.ArgumentParser(description='Gerador de Dados de Usuários e Vendedores')
        parser.add_argument('--generate', type=int, help='Número de documentos a serem gerados')
        parser.add_argument('--output', choices=['mongo', 'json'], help='Destino da saída dos dados')
        parser.add_argument('--connection', type=str, help='String de conexão para o MongoDB')
        parser.add_argument('--filename', type=str, help='Nome do arquivo JSON (sem extensão)')
        args = parser.parse_args()

    # Carrega as configurações do arquivo config.json
    with open('config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)

    if args.generate:
        if args.output == 'mongo':
            asyncio.run(async_main(args, config))
        else:
            sync_main(args, config)
    else:
        data_generator = DataGenerator(config)
        while True:
            try:
                print_main_menu()
                opt = int(input(Fore.YELLOW + "Escolha uma opção: " + Style.RESET_ALL))
            
                if opt == 1:
                    try:
                        docs_count = int(input(Fore.YELLOW + "Quantos documentos deseja gerar? " + Style.RESET_ALL))
                        print_generation_menu()
                        opt = int(input(Fore.YELLOW + "Escolha uma opção: " + Style.RESET_ALL))
                        
                        if opt == 1:
                            # Gera e salva os dados no MongoDB
                            try:
                                logging.info('Generating data and saving to MongoDB')
                                connection_str = input(Fore.YELLOW + 'String de conexão com o MongoDB: ' + Style.RESET_ALL)
                                mongo_handler = MongoDBHandler(connection_str, config["MONGO_DATABASE"], config["MONGO_COLLECTION"])
                                asyncio.run(mongo_handler.connect())
                                
                                users = generate_users_parallel(data_generator, docs_count)
                                asyncio.run(mongo_handler.insert_many(users))
                                sleep(1)
                                cls_message(Fore.GREEN + 'Dados inseridos com sucesso!', delay=2)
                            except Exception as e:
                                logging.error(f"Error: {e}")
                                cls_message(Fore.RED + f"Erro: {e}", delay=3)
                        elif opt == 2:
                            # Gera e salva os dados em um arquivo JSON
                            try:
                                logging.info('Generating data and saving to JSON file')
                                users = generate_users_parallel(data_generator, docs_count)
                                directory = "output_json"
                                if not exists(directory):
                                    makedirs(directory)
                                file_name = input(Fore.YELLOW + 'Nome do arquivo JSON (sem extensão): ' + Style.RESET_ALL) + '.json'
                                file_path = join(directory, file_name)
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    json.dump(users, f, ensure_ascii=False, indent=4, default=data_generator.json_serial)
                                cls_message(Fore.GREEN + f'Dados salvos com sucesso em {file_path}!', delay=2)
                            except Exception as e:
                                logging.error(f"Error saving to JSON file: {e}")
                                cls_message(Fore.RED + f'Erro ao salvar o arquivo JSON: {e}', delay=3)
                    except ValueError:
                        logging.error('Invalid value for number of documents')
                        cls_message(Fore.RED + 'Valor inválido para a quantidade de documentos!', delay=3)
                elif opt == 2:
                    # Sai do programa
                    logging.info('Exiting program')
                    cls_message(Fore.RED + 'Saindo do sistema...', delay=2)
                    exit()
                else:
                    logging.warning('Invalid option selected')
                    cls_message(Fore.RED + 'Opção inválida', delay=2)
            
            except ValueError:
                logging.error('Invalid value entered')
                cls_message(Fore.RED + 'Valor inválido!', delay=2)
            except Exception as e:
                logging.error(f'Unexpected error: {e}')
                cls_message(Fore.RED + f'Ocorreu um erro inesperado: {e}', delay=3)

if __name__ == "__main__":
    run_main()
