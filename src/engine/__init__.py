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
        self.template = template.replace('\n', '')
        self.data = data
        self.kwargs = kwargs
        # Compiled regular expressions
        self.conditionalRE = re.compile(r"\{\{\s\D*\s\}\}")
        self.loopRE = re.compile(r"\{\:\s\D*\s\:\}")

    def render(self) -> str:
        """
            Render the template
        """
        self.replaceLoops()
        self.replaceConditionals()
        self.replaceVariables()
        return self.template.replace('>', '>\n')

    def replaceVariables(self):
        """
            This function is used to replace the variables in the template with the actual data
        """
        # store temporary template variable to mutate this instead of directly mutating the global template
        template = self.template
        # Get count of variables
        count = template.count('{[')
        # Iterate through the variables
        while count > 0:
            # Get the variable
            var = template.split('{[')[1].split(']}')[0]
            # Check for type of the key
            if( '[' in var ):
                # Get the key
                key = var.split('[')[0].strip()
                # Get the index
                index = var.split('[')[1].split(']')[0]
                # Replace the variable with the data
                if isinstance(self.data[key], list):
                    template = template.replace('{[' + var + ']}', f'{self.data[key][int(index)]}')
                elif isinstance(self.data[key], dict):
                    template = template.replace('{[' + var + ']}', f'{self.data[key][index]}')
                else:
                    raise DataNotIterable(self.data, key)


            else:
                # Replace the variable
                template = template.replace('{[' + var + ']}', f'{self.data[var.strip()]}')
            count -= 1
        self.template = template

    
    def replaceConditionals(self):
        """
            This Function is user to parse the conditionals and logical keep the snippets or removes them
        """
        template = self.template
        finds = self.conditionalRE.findall(template)
        print(finds)
        for find in finds:
            find = find.split('}}')
            self.parseCondition(find[0])
            rem = find[1].replace('{{ end ', '')
            print(rem)
        
    def parseCondition(self, con: str) -> str:
        # clean the given condition string
        con = con.replace('{{ ', '').replace('"', '')
        conParts = con.split(' ')
        print(conParts)

        
        
    
    def replaceLoops(self):
        """
            This function is used to parse the loops in the template and boil them done to variables only statements

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
            # Removing unnecessary spaces
            find.strip()
            # Checking if the string actually starts from a loop
            if '{{' in find:
                indexOfCon = find.index('{{ end }}')
                find = find[indexOfCon + 9 : :]
            # Get the variables
            var, data, slice, skip = self.parseLoopStatement(find)
            # Start of the loop statement
            index = template.index(find)
            # End of the loop block
            endIndex = template.index('{: end :}')
            # Slice of template before the loop statement
            firstHalf = template[: index :]
            # Slice of template after the loop block
            secondHalf = template[endIndex + 9 : :]
            # Checking if the key is iterable (currently only lists are iterable)
            if isinstance(self.data[data], list):
                # Iterate through the list
                for item in range(len(self.data[data])):
                    firstHalf += slice.replace(var, f'{data}[{item}]')
            elif isinstance(self.data[data], dict):
                # Iterate through a dictionary
                for keys in self.data[data].keys():
                    firstHalf += slice.replace(var, f'{data}[{keys}]')

            # Replace the template with the new template
            template = firstHalf + secondHalf
        self.template = template
            
    def parseLoopStatement(self, find):
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
        # Extracting the loop block
        slice = loopArray.pop()
        # Extracting the loop statement
        condition = loopArray[0].split(' ')
        # Extracting the variable
        var = condition[-4]
        data = condition[-2]
        return var, data, slice, lenCondition