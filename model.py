from langchain.chat_models.gigachat import GigaChat
from langchain.agents import AgentExecutor, create_gigachat_functions_agent

from agent_tools import ClassesExtractTool, CVPredictTool, ImagePathsTool, InfoTool

with open("credentials.txt", 'r') as f:
    credentials = f.read()

giga = GigaChat(
    credentials=credentials, 
    scope="GIGACHAT_API_PERS", 
    model="GigaChat",
    function_call=True,
    verify_ssl_certs=False
)

tools = [ClassesExtractTool(), CVPredictTool(), ImagePathsTool(), InfoTool()]
agent = create_gigachat_functions_agent(giga, tools)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)