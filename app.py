import autogen


config_list=[
    {
        "model": "doesn't matter",
        "base_url": "http://localhost:1234/v1",
        "api_key": "doesn't matter"
    }
]

llm_config ={
    "timeout":600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
    "max_tokens": -1
}

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=7,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    #code_execution_config={"work_dir":"web","use_docker":False},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task ="""
Transform the COBOL file located at "C:\old anaconda\Desktop\eglm\C.cbl" into an equivalent Python script. Ensure that the resulting Python script accurately represents the logic and functionality of the original COBOL code, adhering to Python syntax and conventions. Save the generated Python file in the specified directory that is located at "C:\old anaconda\Desktop\eglm\pyy"
"""
user_proxy.initiate_chat(
    assistant,
    message=task
)

