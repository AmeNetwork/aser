import yaml


def chain_of_think(text, chat_function):

    history_text = ""
    plan_text = ""
    pre_messages = []
    history = []
    planning = []
    result = []

    is_continued = True

    while is_continued:

        prompt = f"""

    You are solving a problem step-by-step.

    Problem: {text}

    History (Previous Step):
    {history_text}

    Current Plan:
    {plan_text}

    Your Tasks:
    1. list all the steps in the planning
    2. choose the step to execute, if the plan is empty, choose the first step
    3. update the plan
    4. decide if the problem is solved (continue:true/false)

    Output YAML format, the output must be in the following format:
    ```yaml
    thinking: <your current step>
    planning: 
      - description: ...
        status: <pending or done>
        result: ...
    is_continued: <true or false>
    ```
    """

        response = chat_function(prompt, pre_messages)

        result.append(response)

        response_yaml = yaml.safe_load(
            response.replace("```yaml", "").replace("```", "").strip()
        )

        is_continued = response_yaml["is_continued"]
        if is_continued:

            if planning == []:
                planning.extend(response_yaml["planning"])
                plan_text = planning[0]["description"]
                history_text = ""

            else:
                plan_text = planning[len(history)]["description"]
                history_text = history[len(history) - 1]

            history.append(plan_text)

            pre_messages.append(
                {
                    "role": "assistant",
                    "content": response,
                }
            )
            continue
        else:
            return result
