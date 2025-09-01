from swarms import Agent as SwarmsAgent, SequentialWorkflow
from aser import Agent as AserAgent


# AserSwarms is the integration of Aser into Swarms.
# Learn more about Swarms https://github.com/kyegomez/swarms


class AserSwarms(SwarmsAgent):
    def __init__(self, config, *args, **kwargs):

        self.agent = AserAgent(**config)
        super().__init__(*args, **kwargs)

    def run(self, task: str, img=None) -> str:

        result = self.agent.chat(task)
        return result


aser_researcher = AserSwarms({"name": "aser_researcher", "model": "gpt-4o-mini"})
aser_writer = AserSwarms({"name": "aser_writer", "model": "gpt-4o-mini"})
workflow = SequentialWorkflow(agents=[aser_researcher, aser_writer])
final_post = workflow.run("The history and future of artificial intelligence")
print(final_post)
