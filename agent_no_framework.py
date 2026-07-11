from google import genai
from google.genai import types
from pydantic import BaseModel
import json 

class PlanSteps(BaseModel):
    step_name: str

def callmodel(prompt, schema):
    response = chat.send_message(prompt, config = types.GenerateContentConfig(
        response_schema = schema,
        response_mime_type = "application/json",
        system_instruction="Answer within 30 words"
        )
    )
    return response.text



def plan_goal():
    plan_prompt = "Break the goal into clear, numbered steps"
    plans = callmodel(plan_prompt, list[PlanSteps])
    plans = json.loads(plans)
    steps = [ plan['step_name'].strip() for plan in plans if plan['step_name'].strip() ]
    return steps

def run_agent():
    steps = plan_goal()
    for step in steps:
        print(step)


        #execute_step(step)
    print(" \n compled step \n ")

if __name__ == "__main__":
    client = genai.Client()
    model = "gemini-2.5-flash"
    chat = client.chats.create(model=model)
    goal = "Create a 4 year plan for an UCF Statistics and Data Science undergrad"
    print(f"Goal : {goal}")
    modified_goal = f""" You are a virtual agent expert in college advising.
                Your goal is {goal}.
                For now, acknowledge the goal, going forward I will be asking you to create a plan and execute the plans.
                            """
    chat.send_message(modified_goal)
    run_agent()


# run -> plan steps -> execute steps