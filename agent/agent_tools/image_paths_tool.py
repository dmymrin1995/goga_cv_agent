import os

from typing import (
    Optional, 
    Type, 
    Union,
    List)

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.callbacks.manager import (
    CallbackManagerForToolRun
)

class AllFilesInput(BaseModel):
    image_path: str = Field(
        default='../agent/images',
        description="""
            Путь к рабочей папке, ВСЕГДА равно ../agent/images'
        """
    )

class ImagePathsTool(BaseTool):
    name = "image_paths_tool"
    description ="""
        Примает:
            image_path: str  путь к рабочей папке
        Возвращает пути абсолютные пути к изображениям в рабочей папке перечисленные строго через зяпятую.
    """
    args_schema: Type[BaseModel] = AllFilesInput
    
    def _run(
        self, image_path: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ):
        image_path = '../agent/images'
        files = os.listdir(image_path)
        files = [os.path.join(image_path, file) for file in files]
        return ",".join(files)