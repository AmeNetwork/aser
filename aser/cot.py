from pydantic import BaseModel
import json

class StepModel(BaseModel):
    step_id: str
    step_prompt: str


class StepsModel(BaseModel):
    steps: list[StepModel]


class CoT:
    def __init__(self, agent):
        self.agent = agent

    def thinking(self, text, max_iterations=None):
        steps_record = []
        prompt = f"""
            Please list the solution steps for the following problems:
            Problem:{text}
        """
        if max_iterations:
            prompt+=f"""
                Max steps: {max_iterations}
            """
        prompt+="""
            Output:
            List all the steps in JSON format: {{"step_id": "1", "step_prompt": "step_prompt"}}        
        """
        steps_response=self.agent.chat(prompt,response_format=StepsModel)
        steps_json=json.loads(steps_response)
        for step in steps_json["steps"]:
            step_prompt=f"""
                You are {step["step_id"]}.
                Current Task: {step["step_prompt"]}
                Previous Results: {steps_record}
            """
            steps_response=self.agent.chat(step_prompt)
            steps_record.append({
                "step_id": step["step_id"],
                "step_prompt": step["step_prompt"],
                "step_response": steps_response,
            })
            if step["step_id"]==len(steps_record):  
                break
        return steps_record
    def print_steps(self,steps_record):
        for step in steps_record:
            print(f"Step {step['step_id']}: {step['step_prompt']}")
            print(f"Response: {step['step_response']}")
            print("\n")
