import os
import json
import uuid

from agent_tools import *
from cv_inference import make_predict

def save_to_json_file(data, filename='predictions.json'):
    unique_id = str(uuid.uuid4())

    try:
        with open(filename, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {}

    existing_data[unique_id] = data

    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)

class CVPredictInput(BaseModel):
    
    found_clss: str = Field(
        description="""
            Список классов извлеченных из запроса пользователя поиск которых необходимо выполнить.
        """
    )
    files: str = Field(
        description="""
            Список изображений в рабочей папке указанной пользователем или в папке по умолчанию
        """
    )

class CVPredictTool(BaseTool):
    
    name = "cv_predict_tool"
    description ="""
        Поиск необходимых пользователю классов, на изображениях в рабочей папке и сохраняет результаты в JSON файл
        В качестве аргументов принимает два значения:
            found_clss: str - строка с пречеслением всех классов, необходимых пользователю через запятую
            files: str  - строка с перечеслением всех файлов в рабочей папке.
    """
    args_schema: Type[BaseModel] = CVPredictInput
    cls_dict: dict = {
        "0": "person",
        "1": "bicycle",
        "2": "car",
        "3": "motorcycle",
        "4": "airplane",
        "5": "bus",
        "6": "train",
        "7": "truck",
        "8": "boat",
        "9": "traffic light",
        "10": "fire hydrant",
        "11": "stop sign",
        "12": "parking meter",
        "13": "bench",
        "14": "bird",
        "15": "cat",
        "16": "dog",
        "17": "horse",
        "18": "sheep",
        "19": "cow",
        "20": "elephant",
        "21": "bear",
        "22": "zebra",
        "23": "giraffe",
        "24": "backpack",
        "25": "umbrella",
        "26": "handbag",
        "27": "tie",
        "28": "suitcase",
        "29": "frisbee",
        "30": "skis",
        "31": "snowboard",
        "32": "sports ball",
        "33": "kite",
        "34": "baseball bat",
        "35": "baseball glove",
        "36": "skateboard",
        "37": "surfboard",
        "38": "tennis racket",
        "39": "bottle",
        "40": "wine glass",
        "41": "cup",
        "42": "fork",
        "43": "knife",
        "44": "spoon",
        "45": "bowl",
        "46": "banana",
        "47": "apple",
        "48": "sandwich",
        "49": "orange",
        "50": "brocolli",
        "51": "carrot",
        "52": "hot dog",
        "53": "pizza",
        "54": "donut",
        "55": "cake",
        "56": "chair",
        "57": "couch",
        "58": "potted plant",
        "59": "bed",
        "60": "dining table",
        "61": "toilet",
        "62": "tv",
        "63": "laptop",
        "64": "mouse",
        "65": "remote",
        "66": "keyboard",
        "67": "cell phone",
        "68": "microwave",
        "69": "oven",
        "70": "toaster",
        "71": "sink",
        "72": "refrigerator",
        "73": "book",
        "74": "clock",
        "75": "vase",
        "76": "scissors",
        "77": "teddy bear",
        "78": "hair drier",
        "79": "toothbrush"
    }
    
    def _run(
        self, found_clss: str, files: str , run_manager: Optional[CallbackManagerForToolRun] = None
    ):
        if found_clss == 'None':
            found_clss = None
        else:
            filtred_clases = []
            classes_list = found_clss.split(",")
            
            for cls in classes_list:
                for key, val in self.cls_dict.items():
                    if cls.strip() == val:
                        filtred_clases.append(int(key)) 
        files = files.split(",")
        for file in files:
            predicts = make_predict(file, classes=filtred_clases)
            for p in predicts:
                save_to_json_file(p)
        