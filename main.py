from langchain.chat_models.gigachat import GigaChat
from langchain.agents import AgentExecutor, create_gigachat_functions_agent
from langchain.tools import tool
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

giga = GigaChat(
    credentials="", 
    scope="GIGACHAT_API_PERS", 
    model="GigaChat", 
    verify_ssl_certs=False)

# print(giga.invoke("Привет"))

@tool
def search_on_image(path_to_file: str, class_names: str) -> int:
    """
        Находит на изображении объекты заданных классов

    Args:
       path_to_file (str): путь к изображению
       class_names (str): имена классов через запятую
    """
    class_dict = {
        "кошка": 15,
        "собака": 16,
        "люди": 0,
        "рюкзак": 24,
        "человек": 0,
        "person": 0,
        "backpack": 24

    }

    target_classes = []

    for cls in class_names.split(","):
        target_classes.append(class_dict[cls.strip()])


    result = model(path_to_file, save=True, classes=target_classes)

new_tools = [search_on_image]


agent = create_gigachat_functions_agent(giga, new_tools)

agent_executor = AgentExecutor(
    agent=agent,
    tools=new_tools,
    verbose=True,
)

while True:
    user_query = input()
    agent_executor.invoke(
        {"input": user_query}
    )["output"]