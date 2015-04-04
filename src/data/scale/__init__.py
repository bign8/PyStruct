from .. import Variable

__all__ = ['V']

var_range = map(str, range(1, 6))
V = [
    Variable('Class', str),
    Variable('L-Weight', int),
    Variable('L-Dist', int),
    Variable('R-Weight', int),
    Variable('R-Dist', int)
]
