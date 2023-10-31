import datetime
import pydantic_models 
from models import *
import bit
from db import *
from config import WIF, ADR
from pony.orm import db_session



@db_session
def create_wallet(user: pydantic_models.User = None, private_key: str = None, testnet: bool = False):
    if not testnet:
        raw_wallet = bit.Key() if not private_key else bit.Key(private_key)
    else:
        raw_wallet = bit.PrivateKeyTestnet() if not private_key else bit.PrivateKeyTestnet(private_key)
    if user:
        wallet = Wallet(user=user, private_key=raw_wallet.to_wif(), address=raw_wallet.address)
    else:
        wallet = Wallet(private_key=raw_wallet.to_wif(), address=raw_wallet.address)
    flush()
    return wallet


@db_session
def create_user(tg_id: int, nick: str = None):
    if nick:
        user = User(tg_ID=tg_id, nick=nick, create_date=datetime.now(), wallet=create_wallet())
    else:
        user = User(tg_ID=tg_id, created_date=datetime.now(), wallet=create_wallet())
    flush()     
    return user

@db_session
def create_transaction(
    sender: User, 
    amount_btc_without_fee: float, 
    receiver_address: str, 
    fee: float | None = None, 
    testnet: bool = False
):
    wallet_of_sender = bit.Key(sender.wallet.private_key) if not testnet else bit.PrivateKeyTestnet(sender.wallet.private_key)
    sender.wallet.balance = wallet_of_sender.get_balance()  
    if not fee:
        fee = bit.network.fees.get_fee() * 1000    
    amount_btc_with_fee = amount_btc_without_fee + fee  
    if amount_btc_without_fee + fee > sender.wallet.balance:
        return f"Too low balance: {sender.wallet.balance}"
    
   
    output = [(receiver_address, amount_btc_without_fee, 'satoshi')]
    
    tx_hash = wallet_of_sender.send(output, fee, absolute_fee=True)     
    
    transaction = Transaction(sender=sender,
                              sender_wallet=sender.wallet,
                              fee=fee,
                              sender_address=sender.wallet.address,
                              receiver_address=receiver_address,
                              amount_btc_with_fee=amount_btc_with_fee,
                              amount_btc_without_fee=amount_btc_without_fee,
                              date_of_transaction=datetime.now(),
                              tx_hash=tx_hash)
    return transaction  

# wallet = bit.PrivateKeyTestnet(WIF)
# print(f"Balance {wallet.get_balance()}")
# print(f"Address {wallet.address}")
# print(f"Private key {wallet.to_wif()}")
# print(f"All transactions {wallet.get_transactions()}")

# outputs = [("muh9DYMTWXfPEd9zPnfvCS1yX8hPLbkE9e", 0.000001, 'btc')]
# transactions = wallet.send(outputs)
