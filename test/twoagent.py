
# add local autogen to system path
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample
config_list = config_list_from_json(env_or_file="/home/adamsl/autogen/test/MY_CONFIG")
# config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
assistant.llm_config[ "model" ] = "gpt-3.5-turbo" # this has been fixed, but be sure!
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
# user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
# user_proxy.initiate_chat(assistant, message="Act as an expert iOS Developer.  Create an iOS push notification test from the Linux command line on a Mac with Xcode installed." )
# user_proxy.initiate_chat(assistant, message="Act as an Expert C++ Developer and an Expert in Object Oriented Programming.  Examine the project in the directory ``` /home/adamsl/rpi-rgb-led-matrix/tennis-game/ ``` Using ls and cat ( or any other ) Linux command when necessary.  Make a plan to break it up into two testable parts." )

#  user_proxy.initiate_chat( assistant, message="Show the Linux tree output from the directory ``` /home/adamsl/rpi-rgb-led-matrix/tennis-game/ ``` " )