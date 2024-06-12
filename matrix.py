def get_matrices(rows: int, columns: int) -> list:
    """
    This function takes two integers, 'rows' and 'columns', as input and returns a list of lists, representing a matrix.
    Once all the values are entered, the function returns the 'matrix' list.

    :param rows: The number of rows in the matrix
    :param columns: The number of columns in the matrix
    :return: A list of lists, representing the matrix
    """
    matrix = []

    for i in range(rows):
        inner_list = []
        for j in range(columns):
            while True:
                try:
                    value = int(input(f'Enter the value of [{i + 1}] [{j + 1}] : '))
                    inner_list.append(value)
                    break
                except ValueError:
                    print('Invalid input')
        matrix.append(inner_list)
    return matrix


def flatten_matrix(mat):
    print([item for row in mat for item in row])


def add_matrices(matrices1, matrices2):
    """
    This function takes two matrices as input and returns a matrix.
    Then, it iterates through each row and column, adding the corresponding elements of the two matrices.

    :param matrices1: The first matrix
    :param matrices2: The second matrix
    :return: A matrix representing the sum of the two matrices
    """
    row1 = len(matrices1)
    col1 = len(matrices1[0])  # len of the first row
    matrix = []

    for i in range(row1):  # [[1, 2], [3, 4]]
        row = []
        for j in range(col1):  # [[4, 6], [2, 4]]
            row.append(matrices1[i][j] + matrices2[i][j])

        matrix.append(row)

    flatten_matrix(matrix)


def subtract_matrices(matrix1, matrix2):
    """
    This function takes two matrices as input and returns a matrix.
    Finally, the function returns the resulting matrix.

    :param matrix1: The first matrix
    :param matrix2: The second matrix
    :return: A matrix representing the difference of the two matrices
    """

    row2 = len(matrix1)
    col2 = len(matrix1[0])
    matrix = []
    for i in range(row2):
        row = []
        for j in range(col2):
            row.append(matrix1[i][j] - matrix2[i][j])
        matrix.append(row)
    flatten_matrix(matrix)


def multiply_matrix(matrix1, matrix2):
    """
    This function takes two matrices as input and returns a matrix.
    Finally, the function returns the resulting matrix.

    :param matrix1: The first matrix
    :param matrix2: The second matrix
    :return: A matrix representing the product of the two matrices
    """

    matrix = []
    row3 = len(matrix1)
    col3 = len(matrix1[0])

    for i in range(row3):
        row = []
        for j in range(col3):
            row.append(matrix1[i][j] * matrix2[i][j])
        matrix.append(row)

    flatten_matrix(matrix)


def division_matrix(mat1: list, mat2: list):
    """
    This function takes two matrices as input and returns a matrix.
    If the second matrix is singular, it raises an error.
    Finally, the function returns the resulting matrix.

    :param mat1: The first matrix
    :param mat2: The second matrix
    :return: A matrix representing the quotient of the two matrices
    """
    row = len(mat1)
    col = len(mat1[0])
    result = []

    for i in range(row):
        row_list = []
        for j in range(col):
            if mat2[i][j] != 0:
                row_list.append(mat1[i][j] // mat2[i][j])
            else:
                row_list.append(None)
        result.append(row_list)

    flatten_matrix(result)


def display_option():
    options = ['Add matrix', 'Subtract matrix', 'Multiply matrix', 'Divide matrix']
    for index, value in enumerate(options, start=1):
        print(index, '.', value)


while True:
    display_option()
    try:
        choice = int(input('Enter your choice : '))

        if choice == 0:
            print('Ending....')
            break

        if choice in [1, 2, 3, 4]:
            rows = int(input('Rows    : '))
            cols = int(input('Columns : '))
            matrix1 = get_matrices(rows, cols)
            print('--Second matrix--')
            matrix2 = get_matrices(rows, cols)

            if choice == 1:
                add_matrices(matrix1, matrix2)

            elif choice == 2:
                subtract_matrices(matrix1, matrix2)

            elif choice == 3:
                multiply_matrix(matrix1, matrix2)

            elif choice == 4:
                division_matrix(matrix1, matrix2)

            else:
                print('Select a valid choice!')
    except ValueError:
        print('Invalid input!')
