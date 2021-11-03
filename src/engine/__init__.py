class Renderer:
    """
       The actually rendering engine, the various functions here look for:
        - {[ xyz ]} -> to replace with data[xyz]
        - {{ xyx == '45' }} -> compute the conditional
        - {: for y in xyz :} -> for loops
        - {{ xyz|<func> }} -> apply a function to the data
    """
    
    def __init__(self, template, data, **kwargs):
        self.template = template
        self.data = data
        self.kwargs = kwargs

    def render(self):
        raise NotImplementedError