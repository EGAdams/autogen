import autogen
from autogen import config_list_from_json
from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import AssistantAgent

config_list = config_list_from_json(env_or_file="/home/eg1972/autogen/autogen/OAI_CONFIG_LIST")

llm_config = {"config_list": config_list, "cache_seed": 42}


user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    description="This is the user proxy agent.",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,
    },
    human_input_mode="ALWAYS"
)

coder = GPTAssistantAgent(
    name="beta_coder", 
    instructions=AssistantAgent.DEFAULT_SYSTEM_MESSAGE,
    llm_config=llm_config,
    description="This is the coder agent."
)

# Create researcher agent
researcher = GPTAssistantAgent(
    name="researcher",
    llm_config={
        "config_list": config_list_from_json(env_or_file="OAI_CONFIG_LIST"),
        "assistant_id": "asst_G21ehuO6q1ReP5bk3bdpS9fS"
    },
    description="This is the researcher agent."
)
# Make the researcher teachable
# Instantiate the Teachability capability. Its parameters are all optional.
teachability = Teachability(
    verbosity=1,  # 0 for basic info, 1 to add memory operations, 2 for analyzer messages, 3 for memo lists.
    reset_db=False,
    path_to_db_dir="./tmp/interactive/teachability_db",
    recall_threshold=1.5,  # Higher numbers allow more (but less relevant) memos to be recalled.
)

# Now add the Teachability capability to the agent.
teachability.add_to_agent( researcher )

# product manager
product_manager = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Manage ongoing tasks and projects.",
    llm_config=llm_config,
    description="This is the product manager agent."
)

# groupchat = autogen.GroupChat( agents=[ user_proxy, coder, product_manager, researcher ], messages=[], max_round=30 )
groupchat = autogen.GroupChat( agents=[ user_proxy, researcher ], messages=[], max_round=30, allow_repeat_speaker=False )
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager, message="Please ask the Researcher Agent to use the secret code getting tool to get the secret code.  Let me know what it is."
)
# type exit to terminate the chat
