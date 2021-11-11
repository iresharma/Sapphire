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
        """
            This function is used to replace the loops in the template and boil them done to variables only statements

            So the way this works is if we have a loop in the sapphire template that looks like this:
            {: for x in xyz :}
                hi {[ x ]}
            {: end :}
            Then we will replace the loop with the variable representation of the data ( len(xyz) = 3 )
            So the template will look like this:
                hi {[ x[0] ]}
                hi {[ x[1] ]}
                hi {[ x[2] ]}
            now thw replaceVariables function will replace the variables with the actual data
        """
        
        # store temporary template variable to mutate this instead of directly mutating the global template
        template = self.template
        # Find all the loops
        finds = self.loopRE.findall(template)[0].split('{: end :}')
        # pop the last element of the find beacasue it is always empty
        finds.pop()
        for find in finds:
            # Get the variables
            var, data, slice, skip = self.getVariables(find)
            # Start of the loop statement
            index = template.index(find)
            # End of the loop block
            endIndex = template.index('{: end :}')
            # Slice of template before the loop statement
            firstHalf = template[: index :]
            # Slice of template after the loop block
            secondHalf = template[endIndex + 9 : :]
            # Checking if the key is iterable (currently only lists are iterable)
            if type(self.data[data]) != list:
                raise DataNotIterable(self.data, data)
            # Iterate through the list
            for item in range(len(self.data[data])):
                firstHalf += slice.replace(var, f'{data}[{item}]')
            # Replace the template with the new template
            template = firstHalf + secondHalf
        self.template = template
            
    def getVariables(self, find):
        """This function is used to get the variables from the loop
        
        Keyword arguments:
            find -- the loop statement
        Return: 
            var: the variable to be replaced,
            data: the data to be replaced with,
            slice: the slice to be replaced with,
            skip: the number of characters to skip
        """
        # This returns an array where the
        # first element is the loop statement
        # second element is the loop block
        loopArray = find.split(':}')

        # Length of the loop statement
        lenCondition = len(loopArray[0]) + 2
        # Extracting the loop bloack
        slice = loopArray.pop()
        # Extracting the loop statement
        condition = loopArray[0].split(' ')
        # Extracting the variable
        var = condition[-4]
        data = condition[-2]
        return var, data, slice, lenCondition