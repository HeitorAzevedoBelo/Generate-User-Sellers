# Gerador de Dados de Usuários e Vendedores

Este projeto é um gerador de dados de usuários e vendedores que pode salvar os dados gerados em um banco de dados MongoDB ou em um arquivo JSON. Ele inclui uma interface de linha de comando para interagir com o gerador e uma série de testes unitários para garantir que o código funcione corretamente.

## Índice

- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
  - [Linha de Comando](#linha-de-comando)
  - [Menu Interativo](#menu-interativo)
- [Testes](#testes)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Instalação

Para instalar e usar este projeto, siga as etapas abaixo:

1. **Clone o repositório**:

    ```sh
    git clone https://github.com/seu-usuario/gen_users_sellers.git
    cd gen_users_sellers
    ```

2. **Crie um ambiente virtual e ative-o**:

    ```sh
    python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No Linux/Mac
    source venv/bin/activate
    ```

3. **Instale as dependências**:

    ```sh
    pip install -r requirements.txt
    ```

## Configuração

Antes de executar o projeto, configure-o corretamente:

1. **Arquivo de Configuração**:

    Edite o arquivo `config.json` para ajustar as configurações do projeto, como a lista de vendedores, categorias de MCC e tipos de transações.

    ```json
    {
        "SELLERS": ["221512"],
        "MCC_DICT": [
            {"mcc": 5422, "category": "AÇOUGUEIRO"},
            {"mcc": 5462, "category": "PADARIA"},
            {"mcc": 5499, "category": "LOJA DE ALIMENTOS"},
            {"mcc": 5411, "category": "SUPERMERCADO"},
            {"mcc": 5812, "category": "RESTAURANTE"},
            {"mcc": 5814, "category": "FAST FOOD"},
            {"mcc": 5921, "category": "LOJA DE BEBIDAS"},
            {"mcc": 5300, "category": "ATACADISTA"},
            {"mcc": 5441, "category": "CONFEITARIA"},
            {"mcc": 5451, "category": "LOJA DE LATICÍNIOS"}
        ],
        "TRANSACTION_TYPES": ["QRCODE", "PIX", "CARD"]
    }
    ```

## Uso

Você pode usar o projeto de duas maneiras: através da linha de comando ou usando o menu interativo.

### Linha de Comando

Para gerar documentos usando a linha de comando:

- **Salvar no MongoDB**:

    ```sh
    python main.py --generate 10 --output mongo --connection "mongodb://localhost:27017"
    ```

- **Salvar em um arquivo JSON**:

    ```sh
    python main.py --generate 10 --output json --filename "dados"
    ```

### Menu Interativo

Para usar o menu interativo, execute:

```sh
python main.py
```

### Testes
Para executar a bateria de testes unitários, use o comando:

```
python -m unittest discover tests
```

### Estrutura do projeto
Aqui está uma visão geral da estrutura do projeto:

```
    gen_users_sellers/
    │
    ├── data_generator.py         # Módulo responsável pela geração de dados
    ├── main.py                   # Arquivo principal do projeto
    ├── mongodb_handler.py        # Módulo responsável pela interação com o MongoDB
    ├── logger.py                 # Configuração de logging
    ├── config.json               # Arquivo de configuração
    ├── requirements.txt          # Arquivo de dependências
    ├── tests/                    # Pasta contendo os testes unitários
    │   ├── __init__.py
    │   ├── test_data_generator.py
    │   ├── test_mongodb_handler.py
    │   └── test_main.py
    └── README.md                 # Documentação do projeto
```