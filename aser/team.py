from pydantic import BaseModel
import json


class Team:
    def __init__(self, name=None, members=None):
        self.name = name
        self.members = members if members else []

    def get_members(self):
        return self.members

    def get_agent(self, name):
        for member in self.members:
            if member.name == name:
                return member
        return None

    def run(self, mode, task, supervisor=None):
        if mode == "supervisor":
            yaml_propmt = f"""
            ```yaml
            name: {supervisor.name}
            role: supervisor
            duty: {supervisor.description}. Which of the following memebers is the best at this task? Please return its name only.
            task: {task}
            """
            for member in self.members:
                yaml_propmt += f"""
                - name: {member.name}
                  role: member
                  duty:{member.description}
                """
            yaml_propmt += """
            ```
            """
            supervisor_response = supervisor.chat(
                yaml_propmt, response_format=TeamMember
            )
            agent_name = json.loads(supervisor_response)["name"]
            agent_response = self.get_agent(agent_name).chat(task)
            return agent_response
        else:
            return None



class TeamMember(BaseModel):
    name: str
