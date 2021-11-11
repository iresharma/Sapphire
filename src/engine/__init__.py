import re
from errors import DataNotIterable
class Renderer:
    """
       The actually rendering engine, the various functions here look for:
        - {[ xyz ]} -> to replace with data[xyz]
        - {{ xyx == '45' }} -> compute the conditional
        - {: for y in xyz :} -> for loops
        - {{ xyz|<func> }} -> apply a function to the data
    """
    
    def __init__(self, template: str, data: dict or None, **kwargs):
        self.template = template
        self.data = data
        self.kwargs = kwargs
        # Compiled regular expressions
        self.variableRE = re.compile(r"\{\[\s\D\w*\s\]\}")
        self.conditionalRE = re.compile(r"\{\{\s\D\w*\s\}\}")
        self.loopRE = re.compile(r"\{\:\s\D*\s\:\}")

    def render(self) -> str:
        """
            Render the template
        """
        self.replaceLoops()
        return self.template
        # Rendering out the loops

    def replaceLoops(self):
        template = self.template
        finds = self.loopRE.findall(template)[0].split('{: end :}')
        finds.pop()
        for find in finds:
            var, data, slice, skip = self.getVariables(find)
            index = template.index(find)
            endIndex = template.index('{: end :}')
            firstHalf = self.template[:index]
            secondHalf = self.template[endIndex: + 9]
            if type(self.data[data]) != list:
                raise DataNotIterable(self.data, data)
            for item in range(len(self.data[data])):
                firstHalf += slice.replace(var, f'{data}[{item}]')
            self.template = firstHalf + secondHalf
            
    def getVariables(self, find):
        loopArray = find.split(':}')
        lenCondition = len(loopArray[0]) + 2
        loopArray.pop()
        slice = find.split(':}').pop()[1::]
        condition = loopArray[0].split(' ')
        var = condition[-4]
        data = condition[-2]
        return var, data, slice, lenCondition