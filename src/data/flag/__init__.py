from .. import Variable

__all__ = ['V']

convert_2_bool = lambda x: '1' == x

V = [
    Variable('Name'),
    Variable('Landmass', int),
    Variable('Zone', int),
    Variable('Area', int),
    Variable('Population', int),
    Variable('Language', int),
    Variable('Religion', int),
    Variable('Bars', int),
    Variable('Stripes', int),
    Variable('Colors', int),
    Variable('Red', convert_2_bool),
    Variable('Green', convert_2_bool),

    # ...
]
