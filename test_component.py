from core.ame_component import AmeComponent
from web3 import Web3
from eth_account import Account
from eth_abi import encode,decode
from dotenv import load_dotenv
import os
load_dotenv()

component=AmeComponent(
    "http://127.0.0.1:8545",
    "0x29a79095352a718B3D7Fe84E1F14E9F34A35598e"
)
private_key = os.getenv("EVM_PRIVATE_KEY")
account = Account.from_key(private_key)

# types = ["string","uint256"]
# values = ["kevin",10]
# encoded = "0x"+encode(types, values).hex()
#component.send(type="post",name="createUser",params=encoded,value=0,account=account)


# types = ["address"]
# values = [account.address]
# encoded = "0x"+encode(types, values).hex()
# result=component.send(type="get",name="getUser",params=encoded)
# decoded = decode(["string","uint256"], result) 
# print(decoded[0])


# types = ["address","string"]
# values = [account.address,"julia"]
# encoded = "0x"+encode(types, values).hex()
# component.send(type="put",name="updateUserName",params=encoded,value=0,account=account)


component.get_component()