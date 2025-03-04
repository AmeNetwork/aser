from core.social.telegram import TelegramClient
from core.esper import Esper
from core.memory import Memory

memory= Memory(type="sqlite")
esper= Esper(name="esper", model="gpt-4o-mini", description="this is an assistant", memory=memory)

# result=esper.chat("hello")
# print(result)

telegram = TelegramClient(esper) 

telegram.run()
