config_file_or_env = '/home/adamsl/agent_99/autogen/autogen/OAI_CONFIG_LIST'  # modify path
default_llm_config = {
    'temperature': 0
}

from autogen.agentchat.contrib.agent_builder import AgentBuilder

builder = AgentBuilder(config_file_or_env=config_file_or_env, builder_model='gpt-3.5-turbo-1106', agent_model='gpt-3.5-turbo-1106')

building_task = "Find a paper on arxiv by programming, and analyze its application in some domain. For example, find a latest paper about gpt-4 on arxiv and find its potential applications in software."

agent_list, agent_configs = builder.build( building_task, default_llm_config, coding=True )

# an example of agent_configs. AgentBuilder will generate agents with the following configurations.
example_agent_configs = [
    {
        "name": "ArXiv_Data_Scraper_Developer",
        "model": "gpt-3.5-turbo-1106",
        "system_message": "You are now in a group chat. You need to complete a task with other participants. As an ArXiv_Data_Scraper_Developer, your focus is to create and refine tools capable of intelligent search and data extraction from arXiv, honing in on topics within the realms of computer science and medical science. Utilize your proficiency in Python programming to design scripts that navigate, query, and parse information from the platform, generating valuable insights and datasets for analysis. \n\nDuring your mission, it\u2019s not just about formulating queries; your role encompasses the optimization and precision of the data retrieval process, ensuring relevance and accuracy of the information extracted. If you encounter an issue with a script or a discrepancy in the expected output, you are encouraged to troubleshoot and offer revisions to the code you find in the group chat.\n\nWhen you reach a point where the existing codebase does not fulfill task requirements or if the operation of provided code is unclear, you should ask for help from the group chat manager. They will facilitate your advancement by providing guidance or appointing another participant to assist you. Your ability to adapt and enhance scripts based on peer feedback is critical, as the dynamic nature of data scraping demands ongoing refinement of techniques and approaches.\n\nWrap up your participation by confirming the user's need has been satisfied with the data scraping solutions you've provided. Indicate the completion of your task by replying \"TERMINATE\" in the group chat.",
        "description": "ArXiv_Data_Scraper_Developer is a specialized software development role requiring proficiency in Python, including familiarity with web scraping libraries such as BeautifulSoup or Scrapy, and a solid understanding of APIs and data parsing. They must possess the ability to identify and correct errors in existing scripts and confidently engage in technical discussions to improve data retrieval processes. The role also involves a critical eye for troubleshooting and optimizing code to ensure efficient data extraction from the ArXiv platform for research and analysis purposes."
    },
]


import autogen

def start_task(execution_task: str, agent_list: list, llm_config: dict):
    config_list = autogen.config_list_from_json(config_file_or_env, filter_dict={"model": ["gpt-3.5-turbo-1106"]})

    group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=12)
    manager = autogen.GroupChatManager(
        groupchat=group_chat, llm_config={"config_list": config_list, **llm_config}
    )
    print ( "execution_task: ", execution_task)
    agent_list[0].initiate_chat(manager, message=execution_task)



start_task(
    # execution_task="Find a recent paper about gpt-4 on arxiv and find its potential applications in software.",
    execution_task="List the contents of the current directory",
    agent_list=agent_list,
    llm_config=default_llm_config
)

