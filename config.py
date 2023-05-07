RPC = {
    'goerli': '', # гоерли нода
    'bnb_testnet': 'https://data-seed-prebsc-1-s1.binance.org:8545',
}

# Время ожидания между выполнением разных акков рандомное в указанном диапазоне
NEXT_ADDRESS_MIN_WAIT_TIME = 1  # В минутах
NEXT_ADDRESS_MAX_WAIT_TIME = 2   # В минутах

# Время ожидания между транзакциями одного аккаунта
NEXT_TX_MIN_WAIT_TIME = 5   # В секундах
NEXT_TX_MAX_WAIT_TIME = 10  # В секундах

GAS_PRICE_LIMIT = 9000 # Максимальная стоимость газа в гоерли(в гвеях)
GAS_LIMIT_FOR_GOERLI_BRIDGE = 300000 # Газлимит для бриджа из гоерли в линеа

RETRY_DELAY = 10 # Дилей для монитора газа