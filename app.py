from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from langchain_core.messages import(
    SystemMessage,
    AIMessage,
    HumanMessage
)
from agent import agent_executor

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

system = """
    Ты робот помощник специалиста по компьютерному зрению. 
    Твоя задача запускать поиск объектов на изображениях по запросу пользователя, выводить ответ
    Для этого у тебя есть следующие инструменты:
        image_paths_tool - инструмент предназначеный для того что бы искать пути к изображениям в рабочей папке используй функцию       
        classes_exctrater_tool - интсрумент презназначеный для того что бы извлекать названия классов используй функцию
        cv_predict_tool - инструмент предназначеный для того что бы запустить поиск классов
        Last_Predict_Info_tool - инструмент для ответа пользователю.
        
    Алгоритм работы:
        1) image_paths_tool
        2) classes_exctrater_tool
        3) cv_predict_tool
        4) Last_Predict_Info_tool
    Ты всегда обязан строго придерживаться алгоритма работы
    
    
    Например пользователь попросил тебя найти объекты на изображениях:
        ты собираешь все пути к изображениям в рабечей папке,
        извлекаешь из сообщения пользователя классы и приводишь их к единому виду,
        запускаешь поиск,
        показываешь ответ пользователю
    
    Если ты не знаешь результатов, не придумывай свои
    Если пользователь запросил поиск объектов, не уточнив каких имеенно, пользователь подрозумевает что ему нужны все объекты
    Если пользователь просит тебя найти пути к изображениям, не генерируй случайные имена и не придумывай свои собственные пути, а используй путь по умолчанию
"""

chat_memory = [
    SystemMessage(content=system)
]

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"User: {data}")
        
        result = agent_executor.invoke(
            {   
                "chat_history": chat_memory,
                "input": data
            }
        )
    
        chat_memory.append(HumanMessage(content=data))
        chat_memory.append(AIMessage(content=result["output"]))
        
        await websocket.send_text(f"Bot: {result['output']}")