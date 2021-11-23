def triangle_area(base: 'length of triangle base', height: 'length of triangle height') -> 'result of base * height / 2':
    return base * height / 2

print(triangle_area.__annotations__)  # call annotations attribute

# {'base': 'length of triangle base', 'height': 'length of triangle height', 'return': 'result of base * height / 2'}