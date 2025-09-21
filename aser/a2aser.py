import uvicorn
try:
    from urllib.parse import urlparse
    from a2a.server.apps import A2AStarletteApplication
    from a2a.server.request_handlers import DefaultRequestHandler
    from a2a.server.tasks import InMemoryTaskStore
    from a2a.server.agent_execution import AgentExecutor, RequestContext
    from a2a.server.events import EventQueue
    from a2a.utils import new_agent_text_message
    from a2a.types import (
        AgentCapabilities,
        AgentCard,
        AgentSkill
    )
except ImportError:
    raise ImportError(
        "you need to install a2a-sdk, please run `pip install a2a-sdk`"
    )


class A2Aser:
    def __init__(self,
                 agent,
                 url="http://localhost:9999/",
                 version="1.0.0",
                 default_input_modes=['text'],
                 default_output_modes=['text'],
                 capabilities = AgentCapabilities(streaming=True),
                 extensions=None,
                 extra_skills_info=[]
                 ):
        self.url=url
        self.agent=agent
        agent_info = agent.get_info()
        skills = []
        for index, tool in enumerate(agent_info["tools_functions"]):

            skill = AgentSkill(
                id=str(index),
                name=tool["function"]["name"],
                description=tool["function"]["description"],
                tags=[tool["function"]["name"]]
            )
            skills.append(skill)

        if extensions:
            capabilities.extensions=extensions

        self.agent_card = AgentCard(
            name=agent_info["name"],
            description=agent_info["description"],
            url=url,
            version=version,
            default_input_modes=default_input_modes,
            default_output_modes=default_output_modes,
            capabilities=capabilities,
            skills=skills
        )



    def run(self):
        request_handler = DefaultRequestHandler(
            agent_executor=A2AserAgentExecutor(self.agent),
            task_store=InMemoryTaskStore(),
        )

        server = A2AStarletteApplication(
            agent_card=self.agent_card,
            http_handler=request_handler
        )

        parsed = urlparse(self.url)
        host = parsed.hostname
        port = parsed.port
        uvicorn.run(server.build(), host=host, port=port)


class A2AserAgentExecutor(AgentExecutor):

    def __init__(self, agent):
        self.agent = agent

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        user_input = context.get_user_input()
        result = self.agent.chat(user_input)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')
