import autogen
from autogen import config_list_from_json
from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import AssistantAgent
from pydantic import BaseModel, Field   # for spoon feeding and 
from typing import Annotated            # hand holding the function callers


#<file_writer description="Writes content to a specified file."  extends="BaseModel">
class FileInput( BaseModel ):
    filename: Annotated[ str, Field( description="The name of the file to write to." )]
    content:  Annotated[ str, Field( description="The content to write to the file." )]


def write_file(input: Annotated[ FileInput, "Input for writing to a file." ]) -> str:
    """Writes content to a specified file.
    
    Args:
        input (FileInput): The input containing the filename and content.
        
    Returns:
        str: A message indicating the file was written successfully.
    """
    
    with open( input.filename, 'w' ) as file:
        file.write( input.content )

    return "File written successfully."
#</file_writer>


config_list = config_list_from_json(env_or_file="/home/eg1972/autogen/autogen/OAI_CONFIG_LIST")
llm_config = { "config_list": config_list, "cache_seed": 42 }

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

# Create planner agent
planner = GPTAssistantAgent(
    name="planner",
    llm_config={
        "config_list": config_list_from_json(env_or_file="OAI_CONFIG_LIST"),
        "assistant_id": "asst_D7TQNQAMxTpxFmn4XyQKgcCl" # Planner
    },
    description="The planner agent understands the progress of the project, remembers what solutions worked, what solutions didn't work and figures out what to try next without repeating things that we have already tried."
)

#<tools description="a write file tool that writes content to the local hard drive>"
# register the write file too
planner.register_for_llm( name="write_file", description="A write_file tool that writes content to a local file")(
    write_file
)
user_proxy.register_for_execution( name="write_file")( write_file )
#</tools>

# <add_superpower description="gives the agent the capability to remember stuff">
# Make the planner teachable
# Instantiate the Teachability capability. Its parameters are all optional.
teachability = Teachability(
    verbosity=0,  # 0 for basic info, 1 to add memory operations, 2 for analyzer messages, 3 for memo lists.
    reset_db=False,
    path_to_db_dir="/mnt/chromeos/removable/SD Card/chroma_memory/planner_memory_db",
    recall_threshold=1.5,  # Higher numbers allow more (but less relevant) memos to be recalled.
)
# Now add the Teachability capability to the agent.
teachability.add_to_agent( planner )
#</add_superpower>

# product manager
product_manager = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Manage ongoing tasks and projects.",
    llm_config=llm_config,
    description="This is the product manager agent."
)

# file system manager
file_system_manager = autogen.AssistantAgent(
    name="file_system_manager",
    system_message="Manage ongoing tasks and projects.",
    llm_config=llm_config,
    description="The file system manager interacts with the file system."
)

# groupchat = autogen.GroupChat( agents=[ user_proxy, coder, product_manager, planner ], messages=[], max_round=30 )
# groupchat = autogen.GroupChat( agents=[ user_proxy, coder, product_manager, planner ], messages=[], max_round=30 )
groupchat = autogen.GroupChat( agents=[ user_proxy, planner ], messages=[], max_round=30, allow_repeat_speaker=False )
manager = autogen.GroupChatManager( groupchat=groupchat, llm_config=llm_config )

user_proxy.initiate_chat(
    manager, message="Please let me know your name and purpose."
)
# type exit to terminate the chat
