from .. import Variable

__all__ = ['V']

convert_2_bool = lambda x: '1' == x

V = [
    Variable('Name'),
    Variable('Landmass', int),
    Variable('Zone', int),
    None,  # Area
    None,  # Population
    Variable('Language', int),
    Variable('Religion', int),
    # Variable('Bars', int),
    # Variable('Stripes', int),
    # Variable('Colors', int),
    # Variable('Red', convert_2_bool),
    # Variable('Green', convert_2_bool),
    # Variable('Blue', convert_2_bool),
    # Variable('Gold', convert_2_bool),
    # Variable('White', convert_2_bool),
    # Variable('Black', convert_2_bool),
    # Variable('Orange', convert_2_bool),
    # None,
    # Variable('Circles', int),
    # Variable('Crosses', int),
]

V += [None] * (30 - len(V))
