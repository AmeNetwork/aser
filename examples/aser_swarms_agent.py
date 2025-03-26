from swarms import Agent as SwarmsAgent
from aser import Agent as AserAgent

"""
AserSwarms is the integration of Aser into Swarms.
Learn more about Swarms https://github.com/kyegomez/swarms
"""


class AserSwarms(SwarmsAgent):
    def __init__(self,config, *args, **kwargs):

        self.agent = AserAgent(**config)
        super().__init__(*args, **kwargs)

    def run(self, task: str) -> str:

        result = self.agent.chat(task)
        return result


aser_swarms_agent = AserSwarms({"name": "aser_swarms_agent", "model": "gpt-3.5-turbo"})

output = aser_swarms_agent.run("What is bitcoin?")

print(output)
