import uuid
from dataclasses import dataclass
import datetime

import pyqiwi

from data.config import QIWI_TOKEN, WALLET_QIWI, QIWI_PUBKEY

wallet = pyqiwi.Wallet(token=QIWI_TOKEN, number=WALLET_QIWI)


class NotEnoughMoney(Exception):
    pass


class NoPaymentFound(Exception):
    pass


@dataclass
class Payment:
    amount: int

    # Идентефикатор платежа
    id: str = None

    def create(self):
        self.id = str(uuid.uuid4())

    def check_payment(self):
        start_date = datetime.datetime.now() - datetime.timedelta(days=2)
        transactions = wallet.history(start_date=start_date).get("transactions")
        for transaction in transactions:
            if transaction.comment:
                # проверка на наличие оплаты
                if str(self.id) in transaction.comment:
                    # проверка на наличие подходящей суммы
                    if float(transaction.total.amount >= float(self.amount)):
                        return True
                    else:
                        raise NotEnoughMoney
        else:
            raise NoPaymentFound

    # создание ссылки на оплату
    @property
    def invoice(self):
        link = "https://oplata.qiwi.com/create?publicKey={pubkey}&amount={amount}&comment={comment}"
        return link.format(pubkey=QIWI_PUBKEY, amount = self.amount, comment = self.id)
