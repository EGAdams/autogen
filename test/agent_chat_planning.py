
# add local autogen to system path
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, config_list_openai_aoai

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample
config_list = config_list_from_json(env_or_file="/home/adamsl/autogen/test/MY_CONFIG")
# config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")


planner = AssistantAgent(
    name="planner",
    llm_config={"config_list": config_list},
    # the default system message of the AssistantAgent is overwritten here
    system_message="You are a helpful AI assistant. You suggest coding and reasoning steps for another AI assistant to accomplish a task. Do not suggest concrete code. For any action beyond writing code or reasoning, convert it to a step that can be implemented by writing code. For example, browsing the web can be implemented by writing code that reads and prints the content of a web page. Finally, inspect the execution result. If the plan is not good, suggest a better plan. If the execution is wrong, analyze the error and suggest a fix."
)
planner.llm_config[ "model" ] = "gpt-3.5-turbo-0613" # this has been fixed, but be sure!

planner_user = UserProxyAgent(
    name="planner_user",
    max_consecutive_auto_reply=0,  # terminate without auto-reply
    human_input_mode="NEVER",
)
# planner_user.llm_config[ "model" ] = "gpt-3.5-turbo" # this has been fixed, but be sure!

def ask_planner(message):
    planner_user.initiate_chat(planner, message=message)
    # return the last message received from the planner
    return planner_user.last_message()["content"]


# create an AssistantAgent instance named "assistant"
assistant = AssistantAgent(
    name="assistant",
    llm_config={
        "temperature": 0,
        "request_timeout": 600,
        "seed": 42,
        "model": "gpt-3.5-turbo",
        "config_list": config_list_openai_aoai(exclude="aoai"),
        "functions": [
            {
                "name": "ask_planner",
                "description": "ask planner to: 1. get a plan for finishing a task, 2. verify the execution result of the plan and potentially suggest new plan.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "question to ask planner. Make sure the question include enough context, such as the code and the execution result. The planner does not know the conversation between you and the user, unless you share the conversation with the planner.",
                        },
                    },
                    "required": ["message"],
                },
            },
        ],
    }
)
assistant.llm_config[ "model" ] = "gpt-3.5-turbo-0613" # this has been fixed, but be sure!

# create a UserProxyAgent instance named "user_proxy"
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    # is_termination_msg=lambda x: "content" in x and x["content"] is not None and x["content"].rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "planning"},
    function_map={"ask_planner": ask_planner},
)
# user_proxy.llm_config[ "model" ] = "gpt-3.5-turbo" # this has been fixed, but be sure!

# the assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message="""List all the files in the current directory.""",
)