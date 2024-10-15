import json
from agent_tools import *

def get_latest(data: dict):
    latest = max(value['predict_time'] for value in data.values())
    return latest

def get_latest_predict(db_path: str):
    with open("./predictions.json", 'r') as f:
        data = json.load(f)
        
    latest_date = get_latest(data)
    latest_predictions = {
        key: value for key, value in data.items()
        if value['predict_time'] == latest_date
    }
    
    return latest_predictions

class InfoInput(BaseModel):
    db_path: str = Field(
        default='predictions.json',
        description="""
            Путь к базе с результатами поиска объектов на изображениях
        """
    )


class LastPredictInfoTool (BaseTool):
    
    name = "Last_Predict_Info_tool"
    description ="""
        Примает:
            db_path: str  путь к json файлу, с результатами поиска
        
        Инструмент предназначет для вывода пользователю результатов поиска.
        
        Пример результата поиска:
        "83e6b5ba-26e3-410d-99ff-3a5fb204558b": {
            "predict_time": "2024-10-08 15:41:33",
            "image": {
                "name": "img.jpg",
                "objects": [
                    {
                        "object0": {
                            "class": "cat",
                            "cofidence": 0.6
                        }
                    },
                    {
                    "object1": {
                        "class": "car",
                        "cofidence": 0.83
                        }
                    },
                ]
            }
        }
        
        Ответ пользователю всегда должен выглядеть так:
        На изображении {predict_id["image"]["name"]} я нашел следующией объекты:
            {object0['class']} с достоверностью {object0['cofidence']}
            {object1['class']} с достоверностью {object1['cofidence']}
            {object2['class']} с достоверностью {object3['cofidence']}
        
        На изображении {predict_id["image"]["name"]} я нашел следующией объекты:
            {object0['class']} с достоверностью {object0['cofidence']}
            {object1['class']} с достоверностью {object1['cofidence']}
            {object2['class']} с достоверностью {object3['cofidence']}
    """
    args_schema: Type[BaseModel] = InfoInput
    
    def _run(
        self, db_path: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ):
        latest_predict = get_latest_predict(db_path)
        
        return latest_predict