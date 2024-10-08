from typing import Union, List
from datetime import datetime

from ultralytics import YOLO

cv_model: YOLO = YOLO()
NAMES: dict = cv_model.names
def make_predict(
    image: str, classes: Union[List[int], None]=None, save_mode: bool=False
):

    predict = cv_model.predict(image, classes=classes, save=save_mode)
    results_list = []
    # boxes = predict[0].boxes
    for box in predict:
        boxes = box.boxes
        clsses, cofidence = boxes.cls, boxes.conf
        predict_result = {
            'predict_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'image': {
                'name': box.path,
                'objects': []
            }}
        
        for idx, (cls, conf) in enumerate(zip(clsses, cofidence)):
            predict_result['image']['objects'].append({
                f'object{idx}': {
                    'class': NAMES[int(cls.item())],
                    'cofidence': round(conf.item(), 2)
                }
            })
        results_list.append(predict_result)
    return results_list