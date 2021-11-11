import os
from pathlib import Path
from logger import Logger
from engine import Renderer


class Sapphire:
    """
        Sapphire Templating Engine implemented in python, highly inspired by jinja and handlebars
    """
    templates = {}

    def __init__(self, log=True):
        self.__version__ = "0.0.1"
        self.__author__ = "Iresharma"
        self.__email__ = "iresh.sharma8@gmail.com"
        self.OUTPUT_PATH = Path(__file__).parent.parent / "renders"
        self.__log__ = log
        self.logger = Logger()
        # ! Code to reader templates from root of project testing by hardcoding absolute path
        self.read_templates()

    def read_templates(self):
        """
            Reads templates from the root of project
        """
        for root, dirs, files in os.walk("templates"):
            for file in files:
                if(file.split('.')[-1] == 'sph'):
                    self.templates[file.split(
                        '.')[0]] = os.path.join(root, file)
        if(self.__log__):
            self.logger.info(
                f"{len(self.templates.keys())} Template(s) read successfully")

    def renderTemplate(self, templateName: str, data: dict) -> str:
        """
            Renders a template with given data
        """
        if(self.__log__):
            self.logger.info(f"Rendering template {templateName}")
        with open(self.templates[templateName], 'r') as f:
            template = f.read()
            renderer = Renderer(template, data)
            output = renderer.render()
        with open(f'{self.OUTPUT_PATH}/{templateName}.html', 'w') as outFile:
            outFile.write(output)

if __name__ == "__main__":
    sph = Sapphire()
    sph.renderTemplate("base", {"name": "Iresh", 'titles': ['hi', 'hello', 'buy'], 'bonds': [1, 2, 3]})
