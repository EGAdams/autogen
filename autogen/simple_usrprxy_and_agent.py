import autogen
from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import AssistantAgent

config_list = config_list_from_json(env_or_file="/home/adamsl/agent_99/autogen/autogen/OAI_CONFIG_LIST")

llm_config = {"config_list": config_list, "cache_seed": 42}
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,
    },  
    human_input_mode="ALWAYS"
    # human_input_mode="TERMINATE",
)

# coder
# coder = autogen.AssistantAgent(
#     name="Coder",
#     system_message="Help with coding and programming.",
#     llm_config=llm_config,
# )

coder = GPTAssistantAgent(
    name="beta_coder", 
    instructions=AssistantAgent.DEFAULT_SYSTEM_MESSAGE,
    llm_config=llm_config
)

def get_secret_code():
    return "secret_code"

# Create researcher agent
researcher = GPTAssistantAgent(
    name = "researcher",
    llm_config = {
        "config_list": config_list_from_json(env_or_file="OAI_CONFIG_LIST"),
        "assistant_id": "asst_CA1IPBsEq0GIZUwVkHj9vw0s"
    }
)

# product manager
product_manager = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Manage ongoing tasks and projects.",
    llm_config=llm_config,
)

# Create researcher agent
researcher = GPTAssistantAgent(
    name = "researcher",
    llm_config = {
        "config_list": config_list_from_json(env_or_file="OAI_CONFIG_LIST"),
        "assistant_id": "asst_CA1IPBsEq0GIZUwVkHj9vw0s"
    }
)

groupchat = autogen.GroupChat( agents=[ user_proxy, coder, product_manager, researcher ], messages=[], max_round=30 )
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager, message="Please ask the Researcher Agent to use the secret code getting tool to get the secret code.  Let me know what it is."
)
# type exit to terminate the chat
