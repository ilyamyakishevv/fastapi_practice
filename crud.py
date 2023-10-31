import datetime
import pydantic_models
import models
import bit
from config import WIF

wallet = bit.PrivateKeyTestnet(WIF)
print(f"Balance {wallet.get_balance()}")
print(f"Address {wallet.address}")
print(f"Private key {wallet.to_wif()}")
print(f"All transactions {wallet.get_transactions()}")

# outputs = [("muh9DYMTWXfPEd9zPnfvCS1yX8hPLbkE9e", 0.000001, 'btc')]
# transactions = wallet.send(outputs)
