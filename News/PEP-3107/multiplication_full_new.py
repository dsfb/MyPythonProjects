def multiplication(a: dict(description='the multiplicand', type=int), 
                   b: dict(description='the multiplier', type=int)) -> dict(description='the result of multiplying a by b', type=int):
    """Multiply a by b"""
    return a * b


print(multiplication.__annotations__)

#{'a': {'description': 'the multiplicand', 'type': <class 'int'>},
# 'b': {'description': 'the multiplier', 'type': <class 'int'>},
# 'return': {'description': 'the result of multiplying a by b',
#            'type': <class 'int'>}}