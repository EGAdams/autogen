import os
import sys
sys.path.append( './autogen' )
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
# from dotenv import load_dotenv
from dotenv import load_dotenv, find_dotenv

import json
from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent
import autogen


# load_dotenv()
# browserless_api_key = os.getenv("BROWSERLESS_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")
# airtable_api_key = os.getenv("AIRTABLE_API_KEY")
config_list = config_list_from_json("OAI_CONFIG_LIST")


# ------------------ Create functions ------------------ #

# Function for google search
def google_search( search_keyword ):
    print( "running google search for: ", search_keyword )
    print( "jason says \"go get it!\"" )   
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": search_keyword
    })

    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("RESPONSE:", response.text)
    return response.text

# Function for scraping
def summary(objective, content):
    # llm = ChatOpenAI(temperature = 0, model = "gpt-3.5-turbo-16k-0613")
    llm = ChatOpenAI( temperature = 0, model = "gpt-3.5-turbo-1106" )
    

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size = 10000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    
    map_prompt = """
    Write a summary of the following text for {objective}:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "objective"])
    
    summary_chain = load_summarize_chain(
        llm=llm, 
        chain_type='map_reduce',
        map_prompt = map_prompt_template,
        combine_prompt = map_prompt_template,
        verbose = False
    )

    output = summary_chain.run(input_documents=docs, objective=objective)

    return output

def web_scraping(objective: str, url: str):
    print ( "running web scraping for: ", url )
    return "nothing found."
    
def web_scraping_original(objective: str, url: str):
    """
    This function performs web scraping on a specified URL and processes the scraped content.
    It sends a POST request to a web scraping API, retrieves the website's content, and then
    either returns the raw text or provides a summarized version of the content. The decision
    to summarize is based on the length of the content and the specific objective provided by the user.

    Parameters:
    - objective: A string describing the user's original objective or task that guides the content summarization.
    - url: The URL of the website to be scraped.

    The function first attempts to scrape the website content using the provided URL. If the scraping
    is successful and the content's length exceeds a certain threshold (e.g., 10,000 characters), it then
    summarizes the content based on the provided objective. If the content is less than the threshold, 
    the raw text is returned directly.

    Returns:
    - A string containing either the raw text of the website or a summarized version of the content,
      depending on the content's length and the specified objective.
    """
    
    print("*Scraping website...")
    # Define the headers for the request
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }

    # Define the data to be sent in the request
    data = {
        "url": url        
    }

    # Convert Python object to JSON string
    data_json = json.dumps(data)

    # Send the POST request
    response = requests.post(f"https://chrome.browserless.io/content?token={browserless_api_key}", headers=headers, data=data_json)
    
    # Check the response status code
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        print("CONTENT:", text)
        if len(text) > 10000:
            output = summary(objective,text)
            return output
        else:
            return text
    else:
        print(f"HTTP request failed with status code {response.status_code}")    


# Function for get airtable records
def get_records(base_id, table_id):
    print ( "getting records for base_id: ", base_id, " and table_id: ", table_id )
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"

    headers = {
        # 'Authorization': f'Bearer {airtable_api_key}', doesn't know what airtable is
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    print(data)
    return data


# Function for update airtable records

def update_record(base_id, table_id, id, fields):
    print ( "updating record for base_id: ", base_id, " and table_id: ", table_id, " and id: ", id, " and fields: ", fields )
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"

    headers = {
        # 'Authorization': f'Bearer {airtable_api_key}', airtable?
        "Content-Type": "application/json"
    }

    data = {
        "records": [{
            "id": id,
            "fields": fields
        }]
    }

    response = requests.patch(url, headers=headers, data=json.dumps(data))
    data = response.json()
    return data


# ------------------ Create agent ------------------ #

# Create user proxy agent
user_proxy = UserProxyAgent( name="user_proxy",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=1,
    code_execution_config={ "use_docker": 0 },
    system_message="A human admin needed to supervise the commands and function calling.",
    )

# Create researcher agent
researcher = GPTAssistantAgent(
    name = "researcher",
    llm_config = {
        "config_list": config_list_from_json(env_or_file="OAI_CONFIG_LIST"),
        "assistant_id": "asst_CA1IPBsEq0GIZUwVkHj9vw0s"
    }
)

def get_secret_code():
    return "secret_code"

researcher.register_function(
    function_map={
        "get_secret_code": get_secret_code
    }
)

# # Create research manager agent
# research_manager = GPTAssistantAgent(
#     name="research_manager",
#     llm_config = {
#         "config_list": config_list_from_json(env_or_file="OAI_CONFIG_LIST"),
#         "assistant_id": "asst_XeFZYDXE1nupW7VQ7yJesnAL"
#     }
# )

# Create director agent
director = GPTAssistantAgent(
    name = "director",
    llm_config = {
        "config_list": config_list_from_json(env_or_file="OAI_CONFIG_LIST"),
        "assistant_id": "asst_82PXsKbY7SmXsIUyuJUeHzeE",
    }
)


# Create group chat
groupchat = autogen.GroupChat(agents=[user_proxy, researcher, director], messages=[], max_round=15)
group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})


# ------------------ start conversation ------------------ #
# message = """
# Research the funding stage/amount & pricing for each company in the list: https://airtable.com/appj0J4gFpvLrQWjI/tblF4OmG6oLjYtgZl/viwmFx2ttAVrJm0E3?blocks=hide
# """
message = """
Please ask the Researcher Agent to use the secret code getting tool to get the secret code.  Let me know what it is.
"""
user_proxy.initiate_chat(group_chat_manager, message=message)