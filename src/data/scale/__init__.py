from .. import Variable

__all__ = ['V']

var_range = map(str, range(1, 6))
V = [
    Variable('Class', ['L', 'B', 'R'], str),
    Variable('L-Weight', var_range, int),
    Variable('L-Dist', var_range, int),
    Variable('R-Weight', var_range, int),
    Variable('R-Dist', var_range, int)
]
