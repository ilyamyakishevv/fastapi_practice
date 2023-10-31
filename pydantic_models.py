import pydantic
from datetime import datetime


class User(pydantic.BaseModel):
    id : int
    td_ID: int 
    nick: str = None
    created_date: datetime
    wallet: "Wallet"
    sended_transactions: list['Transaction'] = None
    received_transactions: list['Transaction'] = None


class Transaction(pydantic.BaseModel): 
    id: int 
    sender: User = None 
    reciever: User = None
    sender_wallet: 'Wallet' = None
    receiver_wallet: 'Wallet' = None
    sender_address: str 
    receiver_address: str 
    amount_btc_with_fee: float
    amount_btc_without_fee: float
    fee: float
    date_of_transaction: datetime
    tx_hash: str 


class Wallet(pydantic.BaseModel):
    id: int 
    user: User 
    balance: float = 0.0
    private_ker: str 
    address: str 
    sended_transactions: list[Transaction] = []
    received_transactions: list[Transaction] = []

