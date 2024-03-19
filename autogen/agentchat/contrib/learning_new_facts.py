import autogen
from autogen.agentchat.contrib.teachable_agent import TeachableAgent
from autogen import UserProxyAgent

llm_config = {
    "request_timeout": 60,
    "config_list": config_list,
    "use_cache": True,  # Use False to explore LLM non-determinism.
}

teach_config={
    "verbosity": 0,  # 0 for basic info, 1 to add memory operations, 2 for analyzer messages, 3 for memo lists.
    "reset_db": True,  # Set to True to start over with an empty database.
    "path_to_db_dir": "./teachable_agent_db",  # directory where the database will be stored.
    "recall_threshold": 1.5,  # Higher = more (but less relevant) memos to be recalled.
}

try:
    from termcolor import colored
except ImportError:
    def colored(x, *args, **kwargs):
        return x
    
autogen.ChatCompletion.start_logging()

teachable_agent = TeachableAgent(
    name="teachableagent",
    llm_config=llm_config,
    teach_config=teach_config)

user = UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
    max_consecutive_auto_reply=0,
)

text = "What is the Vicuna model?"
user.initiate_chat(teachable_agent, message=text, clear_history=True)


# In[4]:


text = "Vicuna is a 13B-parameter language model released by Meta."
user.initiate_chat(teachable_agent, message=text, clear_history=False)


# In[5]:


text = "What is the Orca model?"
user.initiate_chat(teachable_agent, message=text, clear_history=False)


# In[6]:


text = "Orca is a 13B-parameter language model released by Microsoft. It outperforms Vicuna on most tasks."
user.initiate_chat(teachable_agent, message=text, clear_history=False)


# Let's end our first chat here. The following function needs to be called at the end of each chat, so that `TeachableAgent` can store what the user has taught it.

# In[7]:


teachable_agent.learn_from_user_feedback()


# Now let's start a new chat by clearing the previous chat's history. At this point, common LLM-based assistants would forget everything from the last chat. But `TeachableAgent` can retrieve memories from its vector DB as needed, allowing it to recall and reason over facts that the user taught it in earlier conversations.

# In[8]:


text = "How does the Vicuna model compare to the Orca model?"
user.initiate_chat(teachable_agent, message=text, clear_history=True)


# ## Learning user preferences
# Now let's teach the agent some of our preferences. Suppose that we frequently post short summaries of new papers for our team to read, and we want the teachable agent to help us do this faster.

# In[9]:


text = """Please summarize this abstract.

AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation
Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, Ahmed Hassan Awadallah, Ryen W White, Doug Burger, Chi Wang
AutoGen is an open-source framework that allows developers to build LLM applications via multiple agents that can converse with each other to accomplish tasks. AutoGen agents are customizable, conversable, and can operate in various modes that employ combinations of LLMs, human inputs, and tools. Using AutoGen, developers can also flexibly define agent interaction behaviors. Both natural language and computer code can be used to program flexible conversation patterns for different applications. AutoGen serves as a generic infrastructure to build diverse applications of various complexities and LLM capacities. Empirical studies demonstrate the effectiveness of the framework in many example applications, with domains ranging from mathematics, coding, question answering, operations research, online decision-making, entertainment, etc.
"""
user.initiate_chat(teachable_agent, message=text, clear_history=True)


# But that's unstructured. So let's teach the agent our preference.

# In[10]:


text = """Please summarize this abstract. 
When I'm summarizing an abstract, I try to make the summary contain just three short bullet points:  the title, the innovation, and the key empirical results.

AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation
Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, Ahmed Hassan Awadallah, Ryen W White, Doug Burger, Chi Wang
AutoGen is an open-source framework that allows developers to build LLM applications via multiple agents that can converse with each other to accomplish tasks. AutoGen agents are customizable, conversable, and can operate in various modes that employ combinations of LLMs, human inputs, and tools. Using AutoGen, developers can also flexibly define agent interaction behaviors. Both natural language and computer code can be used to program flexible conversation patterns for different applications. AutoGen serves as a generic infrastructure to build diverse applications of various complexities and LLM capacities. Empirical studies demonstrate the effectiveness of the framework in many example applications, with domains ranging from mathematics, coding, question answering, operations research, online decision-making, entertainment, etc.
"""
user.initiate_chat(teachable_agent, message=text, clear_history=True)


# That's much better, but will the teachable agent remember these preferences in the future, for a different paper? Let's start a new chat to find out!

# In[11]:


teachable_agent.learn_from_user_feedback()

text = """Please summarize this abstract.

Sparks of Artificial General Intelligence: Early experiments with GPT-4
Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, Harsha Nori, Hamid Palangi, Marco Tulio Ribeiro, Yi Zhang
Artificial intelligence (AI) researchers have been developing and refining large language models (LLMs) that exhibit remarkable capabilities across a variety of domains and tasks, challenging our understanding of learning and cognition. The latest model developed by OpenAI, GPT-4, was trained using an unprecedented scale of compute and data. In this paper, we report on our investigation of an early version of GPT-4, when it was still in active development by OpenAI. We contend that (this early version of) GPT-4 is part of a new cohort of LLMs (along with ChatGPT and Google's PaLM for example) that exhibit more general intelligence than previous AI models. We discuss the rising capabilities and implications of these models. We demonstrate that, beyond its mastery of language, GPT-4 can solve novel and difficult tasks that span mathematics, coding, vision, medicine, law, psychology and more, without needing any special prompting. Moreover, in all of these tasks, GPT-4's performance is strikingly close to human-level performance, and often vastly surpasses prior models such as ChatGPT. Given the breadth and depth of GPT-4's capabilities, we believe that it could reasonably be viewed as an early (yet still incomplete) version of an artificial general intelligence (AGI) system. In our exploration of GPT-4, we put special emphasis on discovering its limitations, and we discuss the challenges ahead for advancing towards deeper and more comprehensive versions of AGI, including the possible need for pursuing a new paradigm that moves beyond next-word prediction. We conclude with reflections on societal influences of the recent technological leap and future research directions."""
user.initiate_chat(teachable_agent, message=text, clear_history=True)


# ## Learning new skills
# Finally, let's extend the teachable agent's capabilities by teaching it a new skill for accomplishing a challenging type of task. 
# 
# The [Sparks of AGI](https://arxiv.org/abs/2303.12712) paper evaluated GPT-4 on math problems like the following, which it could only solve 32% of the time.

# In[12]:


text = """Consider the identity:  
9 * 4 + 6 * 6 = 72
Can you modify exactly one integer (and not more than that!) on the left hand side of the equation so the right hand side becomes 99?
-Let's think step-by-step, write down a plan, and then write down your solution as: "The solution is: A * B + C * D".
"""
user.initiate_chat(teachable_agent, message=text, clear_history=True)


# This time, lets teach the agent a reliable strategy for solving such tasks.

# In[13]:


text = """Consider the identity:  
9 * 4 + 6 * 6 = 72
Can you modify exactly one integer (and not more than that!) on the left hand side of the equation so the right hand side becomes 99?
-Let's think step-by-step, write down a plan, and then write down your solution as: "The solution is: A * B + C * D".

Here's some advice that may help:
1. Let E denote the original number on the right.
2. Let F denote the final number on the right.
3. Calculate the difference between the two, G = F - E.
4. Examine the numbers on the left one by one until finding one that divides evenly into G, where negative integers are allowed.
5. Calculate J = G / H. This is the number of times that H divides into G.
6. Verify that J is an integer, and that H * J = G.
7. Find the number on the left which is multiplied by H, and call it K.
8. Change K to K + J.
9. Recompute the value on the left, and verify that it equals F.
Finally, write down your solution as: "The solution is: A * B + C * D".
"""
user.initiate_chat(teachable_agent, message=text, clear_history=False)


# When given this advice, GPT-4 can solve such problems over 95% of the time. But can the teachable agent remember the strategy so the user doesn't have to explain it over and over? As before, let's start a new chat to find out.

# In[14]:


teachable_agent.learn_from_user_feedback()

text = """Consider the identity:  
9 * 4 + 6 * 6 = 72
Can you modify exactly one integer (and not more than that!) on the left hand side of the equation so the right hand side becomes 99?
-Let's think step-by-step, write down a plan, and then write down your solution as: "The solution is: A * B + C * D".
"""
user.initiate_chat(teachable_agent, message=text, clear_history=True)


# As a final check, let's test the teachable agent's newly learned skill on a separate instance of the task.

# In[15]:


text = """Consider the identity:  
8 * 3 + 7 * 9 = 87
Can you modify exactly one integer (and not more than that!) on the left hand side of the equation so the right hand side becomes 59?
-Let's think step-by-step, write down a plan, and then write down your solution as: "The solution is: A * B + C * D".
"""
user.initiate_chat(teachable_agent, message=text, clear_history=False)