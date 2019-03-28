import functools
import re 

def compose(*functions):
    def compose2(f, g):
        return lambda *x: f(g(*x))
    return functools.reduce(compose2, functions, lambda x: x)
    
def getNumbers(str : str): 
    array = re.findall(r'[0-9]+', str) 
    if array:
        return int(array[0])
    else:
        return '-'