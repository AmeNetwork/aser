from aser import Workflow,Agent
from aser.toolkits import web3bio,cast
workflow_agent=Agent(
    name="workflow_agent",
    model="gpt-4.1-mini",
    tools=[web3bio,cast]
)
post_caster_workflow=Workflow(workflow_agent,"examples/workflow.yaml")
post_caster_workflow.start()

