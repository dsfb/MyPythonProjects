import math


def column(matrix, index):
    for line in matrix:
        for s_index, elem in enumerate(line):
            if s_index == index:
                yield elem


def matrix_multiplication():
    dimensions_1 = list(map(int, input('Enter size of first matrix:').split(' ')))
    matrix_1 = list()
    print('Enter first matrix:')
    for _ in range(dimensions_1[0]):
        matrix_1.append(list(map(float, input().split(' '))))

    dimensions_2 = list(map(int, input('Enter size of second matrix:').split(' ')))
    matrix_2 = list()
    print('Enter second matrix:')
    for _ in range(dimensions_2[0]):
        matrix_2.append(list(map(float, input().split(' '))))

    print('The result is:')
    for i in range(dimensions_1[0]):
        line = list()
        for j in range(dimensions_2[1]):
            line.append(sum([a * b for a, b in zip(matrix_1[i], column(matrix_2, j))]))
        s = str(line)[1:-1].replace(',', '')
        print(s)


def multiplication():
    dimensions = list(map(int, input('Enter size of matrix:').split(' ')))
    matrix = list()
    print('Enter matrix:')
    for _ in range(dimensions[0]):
        matrix.append(list(map(float, input().split(' '))))
    multiplier = float(input('Enter constant:'))

    print('The result is:')
    matrix_mul = list()
    for i in range(dimensions[0]):
        matrix_mul.append([elem * multiplier for elem in matrix[i]])
        s = str(matrix_mul[-1])
        print(s[1:-1].replace(',', ''))


def addition():
    dimensions_1 = list(map(int, input('Enter size of first matrix:').split(' ')))
    matrix_1 = list()
    print('Enter first matrix:')
    for _ in range(dimensions_1[0]):
        matrix_1.append(list(map(float, input().split(' '))))

    dimensions_2 = list(map(int, input('Enter size of second matrix:').split(' ')))
    matrix_2 = list()
    print('Enter second matrix:')
    for _ in range(dimensions_2[0]):
        matrix_2.append(list(map(float, input().split(' '))))

    if dimensions_1[0] != dimensions_2[0] or dimensions_1[1] != dimensions_2[1]:
        print('The operation cannot be performed.')
    else:
        print('The result is:')
        matrix_sum = list()
        for i in range(dimensions_1[0]):
            matrix_sum.append([a + b for a, b in zip(matrix_1[i], matrix_2[i])])
            s = str(matrix_sum[-1])
            print(s[1:-1].replace(',', ''))


def transpose_matrix():
    print('1. Main diagonal')
    print('2. Side diagonal')
    print('3. Vertical line')
    print('4. Horizontal line')
    choice = int(input('Your choice:'))
    if choice >= 1 or choice <= 4:
        dimensions = list(map(int, input('Enter matrix size:').split(' ')))
        print('Enter matrix:')
        matrix = list()
        for _ in range(dimensions[0]):
            matrix.append(list(map(float, input().split(' '))))

        transposed_matrix = list()

        if choice == 1:
            for j in range(dimensions[1]):
                transposed_matrix.append(list(column(matrix, j)))
        elif choice == 2:
            for j in range(dimensions[1]):
                transposed_matrix.insert(0, list(column(matrix, j))[::-1])
        elif choice == 3:
            for i in range(dimensions[0]):
                transposed_matrix.append(matrix[i][::-1])
        elif choice == 4:
            for i in range(dimensions[0]):
                transposed_matrix.insert(0, matrix[i])

        for i in range(dimensions[0]):
            s = str(transposed_matrix[i])
            print(s[1:-1].replace(',', ''))


def minor(matrix, i, j):
    result = []
    for index, row in enumerate(matrix):
        if index != i:
            single_row = []
            for j_index, elem in enumerate(row):
                if j_index != j:
                    single_row.append(elem)
            result.append(single_row)
    return result


def cofactor_calculation(matrix, i, j):
    multiplier = int(math.pow(-1, i + j))
    return multiplier * determinant_calculation(minor(matrix, i, j))


def determinant_calculation(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    
    result = 0
    for j in range(len(matrix[0])):
        result += matrix[0][j] * cofactor_calculation(matrix, 0, j)
    return result


def matrix_determinant():
    dimensions = list(map(int, input('Enter matrix size:').split(' ')))
    print('Enter matrix:')
    matrix = list()
    for _ in range(dimensions[0]):
        matrix.append(list(map(float, input().split(' '))))
    print('The result is:')
    print(determinant_calculation(matrix))


def inverse_calculation(matrix):
    determinant = determinant_calculation(matrix)
    if determinant == 0:
        return "This matrix doesn't have an inverse."

    cofactor_matrix = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[i])):
            row.append(cofactor_calculation(matrix, i, j))
        cofactor_matrix.append(row)
    
    transposed_cofactor_matrix = []
    for j in range(len(cofactor_matrix[0])):
        transposed_cofactor_matrix.append(list(column(cofactor_matrix, j)))
    
    inverse_matrix = []
    for i in range(len(transposed_cofactor_matrix)):
        inverse_matrix.append([elem / float(determinant) for elem in transposed_cofactor_matrix[i]])
    return inverse_matrix


def inverse_matrix():
    dimensions = list(map(int, input('Enter matrix size:').split(' ')))
    print('Enter matrix:')
    matrix = list()
    for _ in range(dimensions[0]):
        matrix.append(list(map(float, input().split(' '))))
    print('The result is:')
    inverse_matrix = inverse_calculation(matrix)
    for row in inverse_matrix:
        s = str(row)
        print(s[1:-1].replace(',', ''))


option = 1
while option > 0:
    print('1. Add matrices')
    print('2. Multiply matrix by a constant')
    print('3. Multiply matrices')
    print('4. Transpose matrix')
    print('5. Calculate a determinant')
    print('6. Inverse matrix')
    print('0. Exit')
    option = int(input('Your choice: '))
    if option == 1:
        addition()
    elif option == 2:
        multiplication()
    elif option == 3:
        matrix_multiplication()
    elif option == 4:
        transpose_matrix()
    elif option == 5:
        matrix_determinant()
    elif option == 6:
        inverse_matrix()
    print()


