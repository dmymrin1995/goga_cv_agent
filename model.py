from langchain.chat_models.gigachat import GigaChat
from langchain.agents import AgentExecutor, create_gigachat_functions_agent

from agent_tools import ClassesExtractTool, CVPredictTool, ImagePathsTool

giga = GigaChat(
    credentials="ZWMzMWNmZjktNWE5Ny00MTdmLTkwZGUtNTQxZWFmOTE4NTRlOmVkOTFkNDYxLTRlYzktNDBjYy1iY2EwLWYyMGRhZTJiZTVmMA==", 
    scope="GIGACHAT_API_PERS", 
    model="GigaChat",
    function_call=True,
    verify_ssl_certs=False
)

tools = [ClassesExtractTool(), CVPredictTool(), ImagePathsTool()]
agent = create_gigachat_functions_agent(giga, tools)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)