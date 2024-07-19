from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager


# [
#     {
#         "model": "gpt-4",
#         "api_key": "sk-1111"
#     }
# ]

# # Example: reuse your existing OpenAI setup
# from openai import OpenAI

# # Point to the local server
# client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# completion = client.chat.completions.create(
#   model="TheBloke/Llama-2-7B-Chat-GGUF",
#   messages=[
#     {"role": "system", "content": "Always answer in rhymes."},
#     {"role": "user", "content": "Introduce yourself."}
#   ],
#   temperature=0.7,
# )

# print(completion.choices[0].message)

# Chat with an intelligent assistant in your terminal
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
]

while True:
    completion = client.chat.completions.create(
        model="TheBloke/Llama-2-7B-Chat-GGUF",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)
    
    # Uncomment to see chat history
    # import json
    # gray_color = "\033[90m"
    # reset_color = "\033[0m"
    # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
    # print(json.dumps(history, indent=2))
    # print(f"\n{'-'*55}\n{reset_color}")

    print()
    history.append({"role": "user", "content": input("> ")})





config_list = [
    {
        "api_type": "open_ai",
        "api_base": "http://localhost:1234/v1",
        "api_key": "NULL"
    }
]

llm_config = {
    "config_list": config_list,
    "seed": 47,
    "temperature": 0    ,
    "max_tokens": -1,
    "request_timeout": 6000
}

user_proxy = UserProxyAgent(
    name="user_proxy",
    system_message="A human admin.",
    max_consecutive_auto_reply=10,
    llm_config=llm_config,
    human_input_mode="NEVER"
)

content_creator = AssistantAgent(
    name="content_creator",
    system_message="I am a content creator that talks about exciting technologies about AI.  I want to create exciting content for my audience that is about the latest AI technology.  I want to provide in-depth details of the latest AI white papers.",
    llm_config=llm_config,
)

script_writer = AssistantAgent(
    name="Script_Writer",
    system_message="I am a script writer for the Content Creator.  This should be an eloquently written script so the Content Creator can talk to the audience about AI.",
    llm_config=llm_config
)

researcher = AssistantAgent(
    name="Researcher",
    system_message="I am the researcher for the Content Creator and look up the latest white papers in AI.  Make sure to include the white paper Title and Year it was introduced to the Script_Writer.",
    llm_config=llm_config
)

reviewer = AssistantAgent(
    name="Reviewer",
    system_message="I am the reviewer for the Content Creator, Script Writer, and Researcher once they are done and have come up with a script.  I will double check the script and provide feedback.",
    llm_config=llm_config
)

groupchat = GroupChat(
    agents=[user_proxy, content_creator, script_writer, researcher, reviewer], messages=[]
)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message="I need to create a YouTube Script that talks about the latest paper about gpt-4 on arxiv and its potential applications in software.")