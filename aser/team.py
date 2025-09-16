from pydantic import BaseModel
import asyncio
import json


class MemberModel(BaseModel):
    name: str


class ReactiveModel(BaseModel):
    completed: bool
    next_member_name: str
    action: str


class SubTeamModel(BaseModel):
    name: str
    members: list[MemberModel]
    sub_task: str


class HierarchicalModel(BaseModel):
    sub_teams: list[SubTeamModel]
    coordination: str


class Team:
    def __init__(self, name=None, members=None, supervisor=None, mode="router"):
        self.name = name
        self.members = members if members else []
        self.supervisor = supervisor
        self.mode = mode

    def get_members(self):
        return self.members

    def get_agent(self, name):
        for member in self.members:
            if member.name == name:
                return member
        return None

    def run_router(self, task):
        propmt = f"""
            name: {self.supervisor.name}
            role: supervisor
            duty: {self.supervisor.description}. Which of the following memebers is the best at this task? Please return its name only.
            task: {task}
            """
        for member in self.members:
            propmt += f"""
                - name: {member.name}
                  role: member
                  duty:{member.description}
                """

        supervisor_response = self.supervisor.chat(propmt, response_format=MemberModel)
        agent_name = json.loads(supervisor_response)["name"]
        agent_response = self.get_agent(agent_name).chat(task)
        return agent_response

    async def run_parallel(self, task):
        tasks = []
        for member in self.members:
            member_prompt = f"""
                        You are a team member and you need to execute {member.description} related to this task.
                        Task: {task}
                    ```
                    """
            tasks.append(asyncio.to_thread(member.chat, member_prompt))

        agents_result = await asyncio.gather(*tasks)
        supervisor_prompt = f"""
            You are a supervisor. You need to summarize the results of the following agents.
            {agents_result}
            """
        supervisor_response = self.supervisor.chat(supervisor_prompt)
        return supervisor_response

    def run_sequential(self, task):

        results = []
        current_task = task

        for i, member in enumerate(self.members):

            if i == 0:

                member_prompt = f"""
                You are {member.name}, {member.description}.
                Task: {current_task}
                Please provide your analysis/contribution.
                """
            else:

                previous_results = "\n".join(
                    [f"Member {j+1}: {result}" for j, result in enumerate(results)]
                )
                member_prompt = f"""
                You are {member.name}, {member.description}.
                Original Task: {task}
                Previous Results: {previous_results}
                Please build upon the previous work and provide your contribution.
                """

            result = member.chat(member_prompt)
            results.append(result)

        final_summary = self.supervisor.chat(
            f"""
        Summarize the sequential work done by the team:
        Task: {task}
        Results: {results}
        """
        )

        return final_summary

    def run_reactive(self, task, max_iterations=5):

        iteration = 0
        results = []
        current_task = task
        task_completed = False

        while not task_completed and iteration < max_iterations:
            iteration += 1

            status_prompt = f"""
            You are supervising a reactive team. Evaluate the current situation:
            Original Task: {task}
            Current Iteration: {iteration}
            Previous Results: {results}

            members:
            """

            for member in self.members:
                status_prompt += f"""
                - name: {member.name}
                  role: member
                  duty:{member.description}
                """

            status_prompt += """
            
            Decide:
            1. Is the task completed? (yes/no)
            2. Which member should act next? (name)
            3. What specific action should they take?
            
            Respond in JSON format: {{"completed": boolean, "next_member_name": "name", "action": "description"}}
            """

            supervisor_decision = self.supervisor.chat(
                status_prompt, response_format=ReactiveModel
            )
            decision = json.loads(supervisor_decision)

            if decision["completed"]:
                task_completed = True
                break

            next_member = self.get_agent(decision["next_member_name"])
            if next_member:
                action_prompt = f"""
                You are {next_member.name}, {next_member.description}.
                Current Task: {current_task}
                Supervisor's Instruction: {decision["action"]}
                Previous Results: {results}
                
                Please execute the requested action.
                """

                result = next_member.chat(action_prompt)

                results.append(
                    {
                        "iteration": iteration,
                        "member": next_member.name,
                        "action": decision["action"],
                        "result": result,
                    }
                )

        final_summary = self.supervisor.chat(
            f"""
        Provide a final summary of the reactive team's work:
        Task: {task}
        Total Iterations: {iteration}
        All Results: {results}
        """
        )

        return final_summary

    async def run_hierarchical(self, task):

        # The first step: supervisor analyzes the task and creates sub-teams
        analysis_prompt = f"""
        You are a hierarchical supervisor. Analyze this task and create sub-teams:
        Task: {task}

        Available Team Members:
        """

        for member in self.members:
            analysis_prompt += f"""
            - name: {member.name}
              role: member
              duty:{member.description}
            """

        """
        
        Create a hierarchical plan with:
        1. Sub-teams (groups of members)
        2. Sub-tasks for each sub-team
        3. Coordination strategy
        
        Respond in JSON format:
        {{
            "sub_teams": [
                {{"name": "team_name", "members": ["member1", "member2"], "sub_task": "description"}}
            ],
            "coordination": "strategy_description"
        }}
        """

        plan = self.supervisor.chat(analysis_prompt, response_format=HierarchicalModel)
        plan_data = json.loads(plan)

        # Step 2: Execute sub-team tasks
        sub_team_results = []

        for sub_team in plan_data["sub_teams"]:

            sub_team_members = []
            for member in sub_team["members"]:
                sub_team_members.append(self.get_agent(member["name"]))

            if sub_team_members:

                # sub_team_prompt = f"""
                # You are working as a sub-team on: {sub_team["sub_task"]}
                # You duty is: {{member.description}}
                # Team Members: {[member.name for member in sub_team_members]}
                # """

                #  Parallel execution within sub-teams
                sub_tasks = []
                for member in sub_team_members:
                    member_prompt = f"""
                    You are {member.name}, {member.description}.
                    Sub-team Task: {sub_team["sub_task"]}
                    Duty is: {member.description}
                    Please contribute to this sub-task.
                    """
                    sub_tasks.append(asyncio.to_thread(member.chat, member_prompt))

                # Wait for the sub-team to finish
                sub_results = await asyncio.gather(*sub_tasks)

                sub_team_results.append(
                    {
                        "sub_team": sub_team["name"],
                        "task": sub_team["sub_task"],
                        "results": sub_results,
                    }
                )

        # Step 3: supervisor coordinates and integrates the results
        coordination_prompt = f"""
        You are coordinating the hierarchical team results:
        Original Task: {task}
        Coordination Strategy: {plan_data["coordination"]}
        Sub-team Results: {sub_team_results}
        
        # Provide a comprehensive final result that integrates all sub-team contributions.
        # """

        final_result = self.supervisor.chat(coordination_prompt)

        return {
            "hierarchical_plan": plan_data,
            "sub_team_results": sub_team_results,
            "final_result": final_result,
        }

    def run(self, task):
        if self.mode == "router":
            return self.run_router(task)
        elif self.mode == "reactive":
            return self.run_reactive(task)
        elif self.mode == "hierarchical":
            return self.run_hierarchical(task)
        elif self.mode == "parallel":
            return self.run_parallel(task)
        elif self.mode == "sequential":
            return self.run_sequential(task)
        else:
            raise ValueError(f"Unknown mode: {self.mode}")
