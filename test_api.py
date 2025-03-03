from core.api import API
from core.esper import Esper

esper=Esper(name="test",description="test",model="gpt-4o")

api=API(agent=esper)
api.run()