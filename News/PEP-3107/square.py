def square_area(side: 'length of square side') -> 'result of side ** 2':
    return side ** 2

print(square_area.__annotations__)  # call annotations attribute

# {'side': 'length of square side', 'return': 'result of side ** 2'}