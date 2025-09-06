import yaml
import time


class Step:
    def __init__(self, step):
        self.id = step["id"]
        self.input = step["input"]
        self.output = step.get("output", None)
        self.result = None

    def set_result(self, result):
        self.result = result


class Workflow:
    def __init__(self, agent,yaml_file):
        self.agent = agent
        with open(yaml_file, "r") as f:
            workflow_yaml = yaml.safe_load(f)
            self.name = workflow_yaml["workflow"]["name"]
            self.timeout = workflow_yaml["workflow"]["timeout"]
            self.steps = []
            self.step_ouput_map = {}
            for step in workflow_yaml["workflow"]["steps"]:
                self.steps.append(Step(step))

    def start_once(self):
        for step in self.steps:
            if self.step_ouput_map.get(step.id):
                for output in self.step_ouput_map[step.id]:
                    step.input = f"{step.input}\n{output}"
            result = self.agent.chat(step.input)
            step.set_result(result)
            if step.output:
                if step.output not in self.step_ouput_map:
                    self.step_ouput_map[step.output] = []
                self.step_ouput_map[step.output].append(result)
            else:
                print(result)

    def start(self):
        if self.timeout != 0:
            while True:
                self.start_once()
                time.sleep(self.timeout)
        else:
            self.start_once()
