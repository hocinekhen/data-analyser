"""Contains operations related to matrix"""


import abc

import numpy as np
import pandas as pd
from sklearn import preprocessing

# number of digits in the decimal part
FloatPrecision = 4


class Matrix(metaclass=abc.ABCMeta):
    """Matrix class used for wraping the data array and its columns"""
    def __init__(self, matrix, columns):
        self.matrix = matrix
        self.columns = columns

    @property
    def matrix(self):
        return self.__matrix

    @matrix.setter
    def matrix(self, matrix):
        self.__matrix = matrix

    @property
    def columns(self):
        return self.__columns

    @columns.setter
    def columns(self, columns):
        self.__columns = columns

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        np_matrix = np.array(self.matrix).astype(float)
        np_other_matrix = np.array(other.matrix).astype(float)
        if np_matrix.shape != np_other_matrix.shape:
            return False
        np_columns = np.array(self.columns)
        np_other_columns = np.array(other.columns)
        matrix_equal = np_matrix == np_other_matrix
        columns_equal = np_columns == np_other_columns
        if matrix_equal.all() and columns_equal.all():
            return True
        return False


class Operations(metaclass=abc.ABCMeta):
    """
    Includes operations that can be
    performed on matrix
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'drop_columns_except') and
                callable(subclass.drop_columns_except) and
                hasattr(subclass, 'scale_matrix') and
                callable(subclass.scale_matrix) and
                hasattr(subclass, 'merge_columns_average') and
                callable(subclass.merge_columns_average) and
                hasattr(subclass, 'group_by_column') and
                callable(subclass.group_by_column) and
                hasattr(subclass, 'filter_min_max') and
                callable(subclass.filter_min_max) or
                NotImplemented)

    @abc.abstractmethod
    def drop_columns_except(self, matrix: Matrix, columns) -> Matrix:
        """
        remove all the columns from matrix
        except the ones in the columns parameter
        """
        raise NotImplementedError

    @abc.abstractmethod
    def scale_matrix(matrix):
        """Scale the Matrix columns to
         be between -1 and 1"""
        raise NotImplementedError

    @abc.abstractmethod
    def merge_columns_average(matrix, columns_to_merge, new_column_name):
        """
        Merge columns_to_merge of matrix into
        one column named new_column_name
        the new_column will contain the average
         values of the columns_to_merge
        """
        """
        example:
        col1 col2 col3
         2    3    8
         4    5    4
         7    4    6
        Merging col2 and col3 to average_col
        will give us
        col1  average_col
         2     5.5
         4     4.5
         7     5
         because average_col = (col1+col2)/2
        """
        raise NotImplementedError

    @abc.abstractmethod
    def group_by_column(self, matrix, column_to_group):
        """
        Group the matrix based on column_to_group values
        """

        raise NotImplementedError

    @abc.abstractmethod
    def filter_min_max(matrix, column_name, min_value, max_value):
        """
        Return rows that have values between
        min_value and max_value in the column_name
        """

        raise NotImplementedError


class Calculations(metaclass=abc.ABCMeta):
    """
    Includes calculations that can be performed on matrix
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'calculate_correlation') and
                callable(subclass.calculate_correlation) and
                hasattr(subclass, 'calculate_regression') and
                callable(subclass.calculate_regression) or
                NotImplemented)

    @abc.abstractmethod
    def calculate_correlation(self, matrix: Matrix, columns) -> Matrix:
        """
        Calculate the correlation for the matrix based on the given columns
        """
        raise NotImplementedError

    @abc.abstractmethod
    def calculate_regression(self, matrix: Matrix):
        """
        Calculate the linear regression between two first columns
        """
        raise NotImplementedError


class PandasOperations(Operations):
    """
    Perform Matrix Operations using Pandas
    """

    def drop_columns_except(self, matrix: Matrix, columns) -> Matrix:
        """remove columns from Matrix except the ones in columns array"""

        dataframe = pd.DataFrame(data=matrix.matrix, columns=matrix.columns)

        new_dataframe = dataframe.drop(dataframe.columns.difference(
                        np.array(columns)), axis=1)

        new_matrix = Matrix(new_dataframe.to_numpy(), columns)
        return new_matrix

    def scale_matrix(self, matrix: Matrix):
        "scale matrix values between -1 and 1"

        matrix_to_scale = matrix.matrix
        min_max_scaler = preprocessing.MinMaxScaler()

        matrix_scaled = min_max_scaler.fit_transform(
            matrix_to_scale)  # returns numpy array
        Matrix(matrix_scaled, matrix.columns)

    def merge_columns_average(self, matrix, columns_to_merge, new_column_name):
        """merge columns_to_merge specified by the user and merge them\
            by calculating their average, and store it in new_column_name"""

        # get only columns we want to merge
        to_merge = self.drop_columns_except(
            matrix=matrix, columns=columns_to_merge)
        # Calculate average of this columns
        dataframe = pd.DataFrame(data=to_merge.matrix,
                                 columns=to_merge.columns)
        merged_average = pd.DataFrame(data=dataframe.mean(axis=1),
                                      columns=[new_column_name]).round(
                                          decimals=FloatPrecision)

        # construct the new matrix using
        # only the new_column and the columns that
        # are not included in the columns_to_merge
        origin_matrix = pd.DataFrame(
            data=matrix.matrix, columns=matrix.columns)
        remain_matrix = origin_matrix.drop(
            to_merge.columns, axis=1).round(decimals=FloatPrecision)
        new_matrix = remain_matrix.join(
            merged_average).round(decimals=FloatPrecision)
        return Matrix(matrix=new_matrix.to_numpy(), columns=new_matrix.columns)

    def group_by_column(self, matrix, columns_to_group):
        """group matrix rows based on the columns_to_group"""
        dataframe = pd.DataFrame(data=matrix.matrix, columns=matrix.columns)
        grouped_matrix = dataframe.groupby(columns_to_group)
        grouped_matrix = grouped_matrix.mean().reset_index()\
                                       .round(decimals=FloatPrecision)

        matrix_to_return = Matrix(matrix=grouped_matrix.to_numpy(),
                                  columns=grouped_matrix.columns)
        return matrix_to_return

    def filter_min_max(self, matrix, column_name, min_value, max_value):
        """
        Return rows that have values between
        min_value and max_value in the column_name
        """

        dataframe = pd.DataFrame(data=matrix.matrix, columns=matrix.columns)
        query_string = f"{min_value} <= {column_name} <= {max_value}"
        filtered_df = dataframe.query(query_string)

        matrix_to_return = Matrix(matrix=filtered_df.to_numpy(),
                                  columns=filtered_df.columns)
        return matrix_to_return


class PandasCalculations(Calculations):
    """
    Perform Calculations using Pandas
    """

    def calculate_correlation(self, matrix: Matrix, columns) -> Matrix:
        """
        Calculate the correlation for the matrix based on the given columns
        """

        dataframe = pd.DataFrame(data=matrix.matrix, columns=matrix.columns)
        correlation = dataframe[columns].corr().round(decimals=FloatPrecision)
        correlation_array = correlation.to_numpy()
        # we are updating the columns with the correlation datafram
        # because pandas correlation removes the colomns where the correlation
        # is equal or very near to 0
        correlation_matrix = Matrix(
            matrix=correlation_array, columns=correlation.columns)
        return correlation_matrix

    def calculate_regression(self, matrix: Matrix):
        """
        Calculate the regression's coeffient for the matrix based
        on the given columns
        """
        """
        matrix: a matrix of two vectors
        """
        dataframe = pd.DataFrame(data=matrix.matrix, columns=matrix.columns)
        # number of get number of rows in the matrix
        column_size = dataframe.shape[0]
        # First column vector
        first_column = dataframe.iloc[:, 0].values
        # Second column vector
        second_column = dataframe.iloc[:, 1].values
        # mean of first_column and second_column vector
        mean_first_column = np.mean(first_column)
        mean_second_column = np.mean(second_column)

        # calculating cross-deviation and deviation about first_column
        ss_xy = np.sum(second_column * first_column) - \
            column_size * mean_second_column * mean_first_column
        ss_xx = np.sum(first_column * first_column) - \
            column_size * mean_first_column * mean_first_column

        # calculating regression coefficients
        a = ss_xy / ss_xx
        b = mean_second_column - a * mean_first_column

        return {"a": round(a, FloatPrecision), "b": round(b, FloatPrecision)}


class CalculationsHandler():
    """
    Handle all the operations related to the matrix
    with support of different implementations
    """

    def __init__(self, calculations):
        self._calculations = calculations

    def correlation(self, matrix: Matrix, columns) -> Matrix:
        """
        Calculate the correlation for the matrix based on the given columns
        """
        correlation_matrix = self._calculations.calculate_correlation(
            matrix, columns)
        return correlation_matrix

    def regression(self, matrix: Matrix) -> Matrix:
        """
        Calculate the regression of the scaled matrix between -1 and 1
        which is of two columns
        """
        coefficients = self._calculations.calculate_regression(matrix)
        return coefficients


class OperationsHandler():
    """
    Handle all the operations related to the matrix
    with support of different implementations
    """

    def __init__(self, operations):
        self._operations = operations

    def drop_columns_except(self, matrix: Matrix, columns) -> Matrix:
        """
        Calculate the correlation for the matrix based
         on the given columns
        """
        new_matrix = self._operations.drop_columns_except(matrix, columns)
        return new_matrix

    def scale_matrix(self, matrix: Matrix) -> Matrix:
        """Scale the values of a matrix between -1 and 1"""

        matrix_to_scale = matrix.matrix
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(matrix_to_scale)
        new_matrix = Matrix(x_scaled.round(FloatPrecision), matrix.columns)
        return new_matrix

    def merge_columns_average(self, matrix, columns_to_merge, new_column_name):
        """
        Merges the columns_to_merge into a new one called new_column_name
        the new column is obtained by calculating the average\
         of the merged columns
        """
        return self._operations.merge_columns_average(matrix,
                                                      columns_to_merge,
                                                      new_column_name)

    def group_by_column(self, matrix, column_to_group):
        """group the matrix rows based on the column_to_group"""
        return self._operations.group_by_column(matrix, column_to_group)

    def filter_min_max(self, matrix, column_name, min_value, max_value):
        """Returns the matrix with rows that has values between min_value\
            and max_value in the column column_name"""
        return self._operations.filter_min_max(matrix, column_name,
                                               min_value, max_value)
