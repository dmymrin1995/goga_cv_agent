from langchain_core.messages import(
    SystemMessage,
    AIMessage,
    HumanMessage
)

from model import agent_executor

system = """
    Ты робот помощник специалиста по компьютерному зрению. Твоя задача запускать поиск объектов на изображении по запросу пользователя
    Для этого у тебя есть следующие инструменты:
        image_paths_tool - инструмент предназначеный для того что бы искать пути к изображениям в рабочей папке используй функцию       
        classes_exctrater_tool - интсрумент презназначеный для того что бы извлекать названия классов используй функцию
        cv_predict_tool - инструмент предназначеный для того что бы запустить поиск классов 

    Если пользователь просит тебя найти пути к изображениям, не генерируй случайные имена и не выдумывай свои собственные пути а используй путь по умолчанию
"""

chat_memory = [
    SystemMessage(content=system)
]
while True:
    user_query = input("User: ")
    if user_query == "":
        break
    else:
            
        result = agent_executor.invoke(
            {   
                "chat_history": chat_memory,
                "input": user_query
            }
        )
    
    chat_memory.append(HumanMessage(content=user_query))
    chat_memory.append(AIMessage(content=result["output"]))
    
    print(f"Bot: {result['output']}")
    
        
