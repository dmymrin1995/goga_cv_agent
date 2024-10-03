import os

from agent_tools import *

class AllFilesInput(BaseModel):
    image_path: str = Field(
        description="""
            Путь к рабочей папке. По умолчанию папка images
        """
    )

class ImagePathsTool(BaseTool):
    name = "image_paths_tool"
    description ="""
        Возвращает пути до файлов в рабочей папке с изображениями указанной пользователем
        или в папке по умолчанию.
    """
    args_schema: Type[BaseModel] = AllFilesInput
    
    def _run(
        self, image_path: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ):
        files = os.listdir(
            os.path.join(r"C:\Users\dmymrin1995\Documents\goga_cv_agent", image_path)
        )
        
        return ",".join(files)