import os

from agent_tools import *

class AllFilesInput(BaseModel):
    image_path: str = Field(
        default='../images',
        description="""
            Путь к рабочей папке, ВСЕГДА равно ../images'
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
        image_path = '../goga_cv_agent/images'
        files = os.listdir(image_path)
        files = [os.path.join(image_path, file) for file in files]
        return ",".join(files)