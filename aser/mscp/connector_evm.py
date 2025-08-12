from web3 import Web3
class ConnectorEVM:
    def __init__(self, rpc, address,abi,account):
        self.rpc=rpc
        self.address=address
        self.web3 = Web3(Web3.HTTPProvider(rpc))
        self.account=account
        abi =abi
    