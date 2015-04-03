from .. import Variable

__all__ = ['V']

convert_2_bool = lambda x: '1' == x

var_range = map(str, range(1, 6))
V = [
    Variable('Name', [], str),
    Variable('Landmass', range(1, 7), int),
    Variable('Zone', range(1, 5), int),
    Variable('Area', [], int),
    Variable('Population', [], int),
    Variable('Language', range(1,11), int),
    Variable('Religion', range(8), int),
    Variable('Bars', [], int),
    Variable('Stripes', [], int),
    Variable('Colors', [], int),
    Variable('Red', [], convert_2_bool),
    Variable('Green', [], convert_2_bool),

    # ... 
]
