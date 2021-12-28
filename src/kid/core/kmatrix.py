# :coding: utf-8

# Project Modules
from kid.core.kobject import KObject


class KMatrix(KObject):
    """ Class that handles managing and manipulating matrices.

    References:
        * https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy
        * https://stackoverflow.com/questions/67839675/how-to-decompose-a-matrix-in-python-for-maya
        * https://bindpose.com/maya-matrix-based-functions-part-1-node-based-matrix-constraint/
        * https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_py_ref_class_open_maya_1_1_m_matrix_html
        * https://forums.cgsociety.org/t/decomposing-a-maya-matrix/1172636/3
        * https://integratedmlai.com/basic-linear-algebra-tools-in-pure-python-without-numpy-or-scipy/

    """

    # Static Methods
    @staticmethod
    def get_transposed_matrix(matrix):
        """ Returns a transposed matrix.

        Args:
            matrix(list): NxN matrix list

        Returns:
            list
        """
        return list(map(list, zip(*matrix)))

    @staticmethod
    def get_matrix_minor(matrix, row_index, column_index):
        """
        Args:
            matrix(list):
            row_index(int):
            column_index(int):

        Returns:
            list
        """
        return [row[:column_index] + row[column_index + 1:] for row in (matrix[:row_index] + matrix[row_index + 1:])]

    @staticmethod
    def get_zero_matrix(rows, columns):
        """ Returns a matrix filled with zeros.

        Args:
            rows(int): the number of rows the matrix should have
            columns(int): the number of columns the matrix should have

        Returns
            list
        """
        matrix = list()

        while len(matrix) < rows:
            matrix.append(list())

            while len(matrix[-1]) < columns:
                matrix[-1].append(0.0)

        return matrix

    # Class Methods
    @classmethod
    def add_matrix(cls, a, b):
        """ Adds two matrices and returns the sum

        Args:
            a(list): The first matrix
            b(list): The second matrix

        Returns:
            list
        """
        # Section 1: Ensure dimensions are valid for matrix addition
        rows_a = len(a)
        cols_a = len(a[0])
        rows_b = len(b)
        cols_b = len(b[0])

        if rows_a != rows_b or cols_a != cols_b:
            raise ArithmeticError('Matrices are NOT the same size.')

        # Section 2: Create a new matrix for the matrix sum
        result = cls.get_zero_matrix(rows_a, cols_b)

        # Section 3: Perform element by element sum
        for i in range(rows_a):
            for j in range(cols_b):
                result[i][j] = a[i][j] + b[i][j]

        return result

    @classmethod
    def subtract_matrix(cls, a, b):
        """ Subtracts matrix b from matrix a and returns difference

        Args:
            a(list): The first matrix
            b(list): The second matrix

        Returns:
            list
        """
        # Section 1: Ensure dimensions are valid for matrix subtraction
        rows_a = len(a)
        cols_a = len(a[0])
        rows_b = len(b)
        cols_b = len(b[0])

        if rows_a != rows_b or cols_a != cols_b:
            raise ArithmeticError('Matrices are NOT the same size.')

        # Section 2: Create a new matrix for the matrix difference
        result = cls.get_zero_matrix(rows_a, cols_b)

        # Section 3: Perform element by element subtraction
        for i in range(rows_a):
            for j in range(cols_b):
                result[i][j] = a[i][j] - b[i][j]

        return result

    @classmethod
    def multiply_matrix(cls, a, b):
        """ Returns the product of the matrix a * b

        Args:
            a(list): The first matrix - ORDER MATTERS!
            b(list): The second matrix

        Returns:
            list
        """
        # Section 1: Ensure a & b dimensions are correct for multiplication
        rows_a = len(a)
        cols_a = len(a[0])
        rows_b = len(b)
        cols_b = len(b[0])

        if cols_a != rows_b:
            raise ArithmeticError(
                'Number of a columns must equal number of b rows.')

        # Section 2: Store matrix multiplication in a new matrix
        result = cls.get_zero_matrix(rows_a, cols_b)

        for i in range(rows_a):
            for j in range(cols_b):
                total = 0
                for ii in range(cols_a):
                    total += a[i][ii] * b[ii][j]
                result[i][j] = total

        return result

    @classmethod
    def get_identity_matrix(cls, n):
        """ Returns an identity matrix.

        Args:
            n(int): the square size of the matrix

        Returns
            list
        """
        matrix = cls.get_zero_matrix(n, n)

        for i in range(n):
            matrix[i][i] = 1.0

        return matrix

    @classmethod
    def get_matrix_deternminant(cls, matrix):
        """
        Args:
            matrix(list): NxN matrix list

        Returns:
            int
        """
        # base case for 2x2 matrix
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        determinant = 0

        for c in range(len(matrix)):
            determinant += ((-1) ** c) * matrix[0][c] * cls.get_matrix_deternminant(cls.get_matrix_minor(matrix, 0, c))
        return determinant

    @classmethod
    def get_matrix_inverse(cls, matrix):
        """

        Args:
            matrix(list)

        Returns:
            list
        """

        determinant = cls.get_matrix_deternminant(matrix)

        # special case for 2x2 matrix:
        if len(matrix) == 2:
            return [[matrix[1][1] / determinant, -1 * matrix[0][1] / determinant],
                    [-1 * matrix[1][0] / determinant, matrix[0][0] / determinant]]

        # find matrix of cofactors
        cofactors = list()

        for row in range(len(matrix)):
            cofactor_row = list()

            for column in range(len(matrix)):
                minor = cls.get_matrix_minor(matrix, row, column)
                cofactor_row.append(((-1) ** (row + column)) * cls.get_matrix_deternminant(minor))
            cofactors.append(cofactor_row)

        cofactors = cls.get_transposed_matrix(cofactors)

        for row in range(len(cofactors)):
            for column in range(len(cofactors)):
                cofactors[row][column] = cofactors[row][column] / determinant

        return cofactors

    @classmethod
    def get_relative_transform(cls, a, b):
        """ Returns a relative matrix array from two matrics.

        Args:
            a(list)
            b(list)

        Returns:
            list
        """
        if len(a) != len(b):
            raise TypeError("Provided matrices with different lengths.")

        return a * cls.get_matrix_inverse(b)

    # Object Methods
    def __init__(self):
        self._data = list()

    def __str__(self):
        return self.str_formatter(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def __add__(self, other):
        obj = self.__class__()

        if isinstance(other, KMatrix):
            obj.set_data(self.add_matrix(self.as_list(), other.as_list()))
            return obj

        raise ArithmeticError("Invalid type")

    def __sub__(self, other):
        obj = self.__class__()

        if isinstance(other, KMatrix):
            obj.set_data(self.subtract_matrix(self.as_list(), other.as_list()))
            return obj

        raise ArithmeticError("Invalid type")

    def __mul__(self, other):
        obj = self.__class__()

        if isinstance(other, KMatrix):
            obj.set_data(self.multiply_matrix(self.as_list(), other.as_list()))
            return obj

        raise ArithmeticError("Invalid type")

    def data(self):
        return self._data

    def set_data(self, data):
        """ Set the current matrix from a list.

        Args:
            data(list)

        Returns:
            None
        """
        if isinstance(data, list):
            pass
        elif isinstance(data, tuple):
            data = list(data)
        else:
            raise TypeError("Invaild type.")

        self._data = data
        return

    def set(self, row, column, value):
        """ Set the float weight of an element in the matrix array.

        Args:
            row (int)
            column (int)
            value (int, float)

        Returns:
            None
        """
        self._data[row][column] = float(value)
        return

    def get(self, row, column):
        """ Returns a float weight store in the matrix array.

        Args:
            row (int)
            column (int)

        Returns:
            float
        """
        return self._data[row][column]

    def as_list(self):
        return list(self)


if __name__ == "__main__":
    obj = KMatrix.get_zero_matrix(4, 4)
    print(list(obj))
