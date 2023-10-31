import pydantic
import datetime


class User(pydantic.BaseModel):
    id : int
    td_ID: int 
    nick: str = None
    created_date: datetime
    wallet: "Wallet"
    sended_transactions: list['Trasaction'] = None
    received_transactions: list['Trasaction'] = None
