from esper.ame.evm import EVM
class Chat2Web3:
    def __init__(self,vm,account):
        self.vm = vm
        self.account=account
        self.__set()
        
    def __set(self):
        if self.vm == "evm":
            self.onchain = EVM(self.account)
        else:
            raise Exception("vm not supported")
    
    def add(self,name,description,component_method):
        self.onchain.add(name,description,component_method)
        

    def get_onchain(self):
        return self.onchain

    def is_onchain_tool_function(self,function_name):
        return self.onchain.is_onchain_tool_function(function_name)    

    def call(self,function):
        return self.onchain.call(function)
        
