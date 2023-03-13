# CrystalPAY SDK | Python

Использование

```python 

from crystalpay_sdk import *

# Элементное подключение 

from crystalpay_sdk import CrystalPAY, PayoffSubtractFrom, InvoiceType

```

Работа с API (Создание экземпляра класса)

```python 

crystalpayAPI = CrystalPAY("auth_login", "Secret 1", "Secret 2")

```

`При ошибках, выкидывается исключение со списком ошибок.`

<h1>Функции</h1>


Получение информации о кассе
```python

crystalpayAPI.Me.getinfo() -> json

#Пример ответа
# {
#   "id": 123456789,
#   "name": "examplename",
#   "status_level": 2,
#   "created_at": "2020-11-22 12:34:56"
# }

```

Получение информации о методах оплаты
```python

crystalpayAPI.Method.getlist() -> json

#Пример ответа
# {
#   "methods": {
#     "CRYSTALPAY": {
#       "name": "CrystalPAY P2P",
#       "enabled": true,
#       "extra_commission_percent": 0,
#       "minimal_status_level": 0,
#       "currency": "RUB",
#       "commission_percent": 0,
#       "commission": 0
#     },
#     "TEST": {
#       "name": "Test",
#       "enabled": true,
#       "extra_commission_percent": 8,
#       "minimal_status_level": 0,
#       "currency": "RUB",
#       "commission_percent": 0,
#       "commission": 0
#     }
#     ...
#   }
# }

```

Изменение настроек метода оплаты
```python

crystalpayAPI.Method.edit(method, extra_commission_percent, enabled)

```

Получение баланса кассы
```python

crystalpayAPI.Balance.getinfo(hide_empty=False) -> json

#hide_empty - Изначально равен False (Необязательно указывать)

#Пример ответа
# {
#   "balances": {
#     "LZTMARKET": {
#       "amount": 100,
#       "currency": "RUB"
#     },
#     "BITCOIN": {
#       "amount": 0.00005,
#       "currency": "BTC"
#     }
#     ...
#   }
# }

```

Выставление счёта на оплату
```python

crystalpayAPI.Invoice.create(amount, InvoiceType, lifetime, description="TEST", etc..) -> json

# InvoiceType:
# InvoiceType.topup
# InvoiceType.purchase

# Пример вызова

crystalpayAPI.Invoice.create(100, InvoiceType.purchase, 15)

#Пример ответа
# {
#   "id": "123456789_abcdefghij",
#   "url": "https://pay.crystalpay.io/?i=123456789_abcdefghij",
#   "amount": 100,
#   "type": "purchase"
# }

```

Получение информации о счёте
```python

crystalpayAPI.Invoice.getinfo(id) -> json

#Пример ответа
# {
#   "id": "123456789_abcdefghij",
#   "url": "https://pay.crystalpay.io/?i=123456789_abcdefghij",
#   "state": "notpayed",
#   "type": "purchase",
#   "method": null,
#   "required_method": "",
#   "currency": "RUB",
#   "service_commission": 0,
#   "extra_commission": 0,
#   "amount": 100,
#   "pay_amount": 100,
#   "remaining_amount": 100,
#   "balance_amount": 100,
#   "description": "",
#   "redirect_url": "https://crystalpay.io/",
#   "callback_url": "",
#   "extra": "",
#   "created_at": "2023-01-01 00:00:00",
#   "expired_at": "2023-01-03 12:34:56"
# }

```

Создание заявки на вывод средств
```python

crystalpayAPI.Payoff.create(amount, "method", "wallet", PayoffSubtractFrom, amount_currency="RUB", etc..) -> json

# PayoffSubtractFrom:
# PayoffSubtractFrom.balance
# PayoffSubtractFrom.amount

# Пример вызова

crystalpayAPI.Payoff.create(55, "BITCOIN", "Реквизиты кошелька получателя", PayoffSubtractFrom.balance) -> json

#Пример ответа
# {
#   "id": "123456789_dpWminAiaqwTcBOJVlFk",
#   "method": "ETHEREUM",
#   "commission": 0.0015,
#   "amount": 0.002,
#   "rub_amount": 193,
#   "receive_amount": 0.0005,
#   "deduction_amount": 0.002,
#   "subtract_from": "amount",
#   "currency": "ETH"
# }

```

Подтверждение заявки на вывод средств
```python

crystalpayAPI.Payoff.submit(id) -> json

#Пример ответа
# {
#   "id": "123456789_dpWminAiaqwTcBOJVlFk",
#   "state": "processing",
#   "method": "ETHEREUM",
#   "currency": "ETH",
#   "commission": 0.0015,
#   "amount": 0.002,
#   "rub_amount": 193,
#   "receive_amount": 0.0005,
#   "deduction_amount": 0.002,
#   "subtract_from": "amount",
#   "wallet": "examplewallet",
#   "message": "",
#   "callback_url": "",
#   "extra": "",
#   "created_at": "2023-01-01 11:11:11"
# }

```

Отмена заявки на вывод средств
```python

crystalpayAPI.Payoff.cancel(id) -> json

#Пример ответа
# {
#   "id": "123456789_dpWminAiaqwTcBOJVlFk",
#   "state": "canceled",
#   "method": "ETHEREUM",
#   "currency": "ETH",
#   "commission": 0.0015,
#   "amount": 0.002,
#   "rub_amount": 193,
#   "receive_amount": 0.0005,
#   "deduction_amount": 0.002,
#   "subtract_from": "amount",
#   "wallet": "examplewallet",
#   "message": "Canceled",
#   "callback_url": "",
#   "extra": "",
#   "created_at": "2023-01-01 11:11:11"
# }

```

Получение информации о заявке на вывод средств
```python

crystalpayAPI.Payoff.getinfo(id) -> json

#Пример ответа
# {
#   "id": "123456789_dpWminAiaqwTcBOJVlFk",
#   "state": "canceled",
#   "method": "ETHEREUM",
#   "currency": "ETH",
#   "commission": 0.0015,
#   "amount": 0.002,
#   "rub_amount": 193,
#   "receive_amount": 0.0005,
#   "deduction_amount": 0.002,
#   "subtract_from": "amount",
#   "wallet": "examplewallet",
#   "message": "Canceled",
#   "callback_url": "",
#   "extra": "",
#   "created_at": "2023-01-01 11:11:11"
# }

```

Получение информации о заявке на вывод средств
```python

crystalpayAPI.Ticker.getlist() -> json

#Пример ответа
# {
#   "tickers": [
#     "BCH",
#     "BNB",
#     "BTC",
#     "DASH",
#     "ETH",
#     "LTC",
#     "MATIC",
#     "TON",
#     "TRX",
#     "USD",
#     "USDC"
#   ]
# }

```

Получение курса валют по отношению к рублю
```python

crystalpayAPI.Ticker.get(tickers) -> json

#Пример ввода
#tickers = ["BTC", "LTC"]

#Пример ответа
# {
#   "base_currency": "RUB",
#   "currencies": {
#     "BTC": {
#       "price": 1432359
#     },
#     "LTC": {
#       "price": 5755.99
#     }
#   }
# }

```
