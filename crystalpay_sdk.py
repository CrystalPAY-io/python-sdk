import requests
import json
import hashlib

class InvoiceType:

    topup = "topup"
    purchase = "purchase"

class PayoffSubtractFrom:

    balance = "balance"
    amount = "amount"

class crystal_utils:

    ''' Дополнительный класс, содержащий в себе дополнительные функции для работы SDK '''

    ''' Соединяет необязательные параметры с обязательными '''

    def concatParams(self, concatList, kwargs):

        temp = concatList
        
        for key, param in kwargs:
            temp[key] = param

        return temp

    ''' Отправка запроса на API '''

    def requestsApi(self, method, function, params):

        response = json.loads(
                        requests.post(
                            f"https://api.crystalpay.io/v2/{method}/{function}/", 
                            data = params, 
                            headers = {'Content-Type': 'application/json'} 
                        ).text
                    )

        if(response["error"]):
            raise Exception(response['errors'])

        ''' Убираем из JSON ответа сообщения об ошибках '''

        del response["error"]
        del response["errors"]

        return response

class CrystalPAY:

    ''' Гланый класс для работы с CrystalApi '''

    def __init__(self, auth_login, auth_secret, salt):

        ''' Создание подклассов '''

        self.Me = self.Me(auth_login, auth_secret, crystal_utils())
        self.Method  = self.Method(auth_login, auth_secret, crystal_utils())
        self.Balance = self.Balance(auth_login, auth_secret, crystal_utils())
        self.Invoice = self.Invoice(auth_login, auth_secret, crystal_utils())
        self.Payoff  = self.Payoff(auth_login, auth_secret, salt, crystal_utils())
        self.Ticker = self.Ticker(auth_login, auth_secret, crystal_utils())

    class Me:

        def __init__(self, auth_login, auth_secret, crystal_utils):

            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__crystal_utils = crystal_utils

        ''' Получение информации о кассе '''

        def getinfo(self):
        
            response = self.__crystal_utils.requestsApi(
                "me",
                "info",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret
                })
            )

            return response

    class Method:

        def __init__(self, auth_login, auth_secret, crystal_utils):

            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__crystal_utils = crystal_utils

        ''' Получение информации о методах оплаты '''

        def getlist(self):
        
            response = self.__crystal_utils.requestsApi(
                "method",
                "list",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret
                })
            )
                
            return response

        ''' Изменение настроек метода оплаты '''

        def edit(self, method, extra_commission_percent, enabled):
        
            response = self.__crystal_utils.requestsApi(
                "method",
                "edit",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "method": method,
                    "extra_commission_percent": extra_commission_percent,
                    "enabled": enabled
                })
            )
                
            return response

    class Balance:

        def __init__(self, auth_login, auth_secret, crystal_utils):

            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__crystal_utils = crystal_utils
    
        ''' Получение баланса кассы '''
    
        def getinfo(self, hide_empty=False):
        
            response = self.__crystal_utils.requestsApi(
                "balance",
                "info",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "hide_empty": hide_empty
                })
            )

            return response["balances"]

    class Invoice:

        def __init__(self, auth_login, auth_secret, crystal_utils):

            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__crystal_utils = crystal_utils
        
        ''' Получение информации о счёте '''

        def getinfo(self, id):
        
            response = self.__crystal_utils.requestsApi(
                "invoice",
                "info",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "id": id
                })
            )

            return response

        ''' Выставление счёта на оплату '''

        def create(self, amount, type_, lifetime, **kwargs):
        
            response = self.__crystal_utils.requestsApi(
                "invoice",
                "create",
                json.dumps(
                    self.__crystal_utils.concatParams(
                        {
                            "auth_login": self.__auth_login,
                            "auth_secret": self.__auth_secret,
                            "amount": amount,
                            "type": type_,
                            "lifetime": lifetime
                        },
                        kwargs.items()
                    )
                )
            )

            return response

    class Payoff:

        def __init__(self, auth_login, auth_secret, salt, crystal_utils):

            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__salt = salt
            self.__crystal_utils = crystal_utils

        ''' Создание заявки на вывод средств '''

        def create(self, amount, method, wallet, subtract_from, **kwargs):
        
            signature_string = f"{amount}:{method}:{wallet}:{self.__salt}"
            signature = hashlib.sha1(str.encode(signature_string)).hexdigest()

            response = self.__crystal_utils.requestsApi(
                "payoff",
                "create",
                json.dumps(
                    self.__crystal_utils.concatParams(
                        {
                            "auth_login": self.__auth_login,
                            "auth_secret": self.__auth_secret,
                            "signature": signature,
                            "amount": amount,
                            "method": method,
                            "wallet": wallet,
                            "subtract_from": subtract_from
                        },
                        kwargs.items()
                    )
                )
            )

            return response

        ''' Подтверждение заявки на вывод средств '''

        def submit(self, id):
        
            signature_string = f"{id}:{self.__salt}"
            signature = hashlib.sha1(str.encode(signature_string)).hexdigest()

            response = self.__crystal_utils.requestsApi(
                "payoff",
                "submit",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "signature": signature,
                    "id": id,
                })
            )

            return response

        ''' Отмена заявки на вывод средств '''

        def cancel(self, id):
        
            signature_string = f"{id}:{self.__salt}"
            signature = hashlib.sha1(str.encode(signature_string)).hexdigest()

            response = self.__crystal_utils.requestsApi(
                "payoff",
                "cancel",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "signature": signature,
                    "id": id,
                })
            )

            return response

        ''' Получение информации о заявке на вывод средств '''

        def getinfo(self, id):
        
            response = self.__crystal_utils.requestsApi(
                "payoff",
                "info",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "id": id,
                })
            )

            return response

    class Ticker:

        def __init__(self, auth_login, auth_secret, crystal_utils):

            self.__auth_login = auth_login
            self.__auth_secret = auth_secret
            self.__crystal_utils = crystal_utils

        ''' Получение информации о заявке на вывод средств '''

        def getlist(self):
        
            response = self.__crystal_utils.requestsApi(
                "ticker",
                "list",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                })
            )

            return response["tickers"]

        ''' Получение курса валют по отношению к рублю '''

        def get(self, tickers):
        
            response = self.__crystal_utils.requestsApi(
                "ticker",
                "get",
                json.dumps({
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret,
                    "tickers": tickers
                })
            )

            return response
