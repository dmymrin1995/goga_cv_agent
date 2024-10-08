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


class InfoTool (BaseTool):
    
    name = "info_tool"
    description ="""
        Возвращает результаты поиска объектов на изображениях
        Примает:
            db_path: str  путь к json файлу
    """
    args_schema: Type[BaseModel] = InfoInput
    
    def _run(
        self, db_path: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ):
        latest_predict = get_latest_predict(db_path)
        
        return latest_predict