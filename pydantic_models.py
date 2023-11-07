import pydantic
from datetime import datetime
from typing import List, Optional


class User(pydantic.BaseModel):
    id: int
    td_ID: int
    nick: str = None
    created_date: datetime
    wallet: "Wallet"
    sended_transactions: Optional[List['Transaction']] = None
    received_transactions: Optional[List['Transaction']] = None


class Transaction(pydantic.BaseModel):
    id: int
    sender: User = None
    receiver: User = None
    sender_wallet: 'Wallet' = None
    receiver_wallet: 'Wallet' = None
    sender_address: str
    receiver_address: str
    amount_bts_with_fe: float
    amount_btc_without_fee: float
    fee: float
    date_of_transaction: datetime
    tx_hash: str


class Create_Transaction(pydantic.BaseModel):
    tg_ID: int
    receiver_address: str
    amount_btc_without_fee: float


class Wallet(pydantic.BaseModel):
    id: int
    user: User
    balance: float = 0.0
    private_key: str
    address: str 
    transactions: list[Transaction] = []
    received_transactions: list[Transaction] = []


class UserToUpdate(pydantic.BaseModel):
    id: int
    tg_ID:  int = None
    nick:   str = None
    created_date: datetime = None
    wallet: 'Wallet' = None


class UserToCreate(pydantic.BaseModel):
    tg_ID:  int = None
    nick:   str = None



UserToUpdate.update_forward_refs()