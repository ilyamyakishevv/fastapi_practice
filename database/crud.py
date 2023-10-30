import datetime
from . import pydantic_models
import models
import bit
from config import WIF, ADR

wallet = bit.PrivateKeyTestnet(WIF)
print(wallet.get_balance())
