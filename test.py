from core.esper import Esper
from core.ame_component import AmeComponent
from core.memory import Memory
from core.knowledge import Knowledge

#tinydb memory
#memory=Memory(type="tinydb",path="./memory/database/tiny_db.json",limit=3)

#supabase memory
memory=Memory(type="supabase",table="agent_memory",limit=3)

knowledge=Knowledge(name="test",path="./knowledge",query_ns=2)

esper = Esper(name="test", description="test", model="gpt-4o",memory=memory,knowledge=knowledge)

# component = AmeComponent(
#     "http://127.0.0.1:8545", "0x29a79095352a718B3D7Fe84E1F14E9F34A35598e"
# )

# methods = component.get_methods()

# esper.chat2web3("getUserNameByAddress", "when a user want to get user name and age, it will return 2 value, one is name, the one is age", methods["getUser"])
# esper.chat2web3("changeUserNameByAddress", "when a user change his name", methods["updateUserName"])
# result=esper.ask("change my name,kevin,0xa0Ee7A142d267C1f36714E4a8F75612F20a79720")
# result=esper.ask("get user name 0xa0Ee7A142d267C1f36714E4a8F75612F20a79720")

result=esper.ask("what is jack name?")

print(result)