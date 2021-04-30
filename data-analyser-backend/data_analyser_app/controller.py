"""All methods representing data analyser functionalities goes here"""
import re

import numpy as np
from django.conf import settings

from .helpers import exceptions
from .helpers import formatter
from .helpers import validator
# helpers
from .helpers.files_helper import FileWriter, FileSystemStoragePersistance, \
    FileReader, PandasReader
from .helpers.matrix_helper import Matrix, CalculationsHandler, \
    OperationsHandler, PandasCalculations, PandasOperations


NOT_INCLUDED_ERROR_MSG = "specified columns should be included\
     in the matrix's columns"


def write_file(file):
    """store csv file"""
    # mechanism of storing the file can be changed using
    # another PeristanceInterface see helpers/file_helper.py
    fs = FileSystemStoragePersistance()
    file_writer = FileWriter(fs)
    file_name = file_writer.write_file(file, file.name)
    return file_name


def get_matrix_from_file(file_name):
    """convert csv file to Matrix object"""
    file_path = settings.MEDIA_ROOT
    pandas_reader = PandasReader()
    filer_reader = FileReader(pandas_reader)
    matrix = None
    try:
        matrix = filer_reader.csv_to_matrix(file_path, file_name)
    except FileNotFoundError:
        error_message = "inserted file does not exist"
        raise exceptions.ValidationError(error_message)

    return matrix


def get_matrix_object(matrix, columns):
    """constructing object of type Matrix using matrix and columns arrays """
    # check if columns number equals the shape[1] of the matrix
    matrix_columns_number = np.array(matrix).shape[1]
    if matrix_columns_number != len(columns):
        raise ValueError(
            "columns length should equal to the matrix columns number")
    matrix = Matrix(matrix=matrix, columns=columns)
    return matrix


def get_matrix(body, file_name=None):
    """
    accepts
    body:{
        "is_in_body":boolean,
        "matrix": Matrix
    }
    file_name: string
    -----
    returns a matrix object depneding on the body parameter
    ------
    raise ValidationError
    """
    # get matrix object based on is_in_body parameters
    # if is_in_body true then construct the matrix object
    # from the body parameter
    matrix_is_in_body = body["is_in_body"]
    matrix_object = None

    if matrix_is_in_body:
        matrix_from_body = body["matrix"]
        matrix = matrix_from_body['matrix']
        columns = matrix_from_body['columns']
        matrix_object = get_matrix_object(matrix=matrix, columns=columns)
    else:
        if not file_name:
            raise exceptions.ValidationError(
                message="file name should be inserted")
        matrix_object = get_matrix_from_file(file_name=file_name)
    return matrix_object


def get_cells_columns(columns):
    """
    Retrieves the list of cells names that are not side effect
    which means only the cells that has parameter _x
    it includes the target cell name
    """

    parameter_prefix = "_x"
    suffix = "L"

    # retrieve the list of cells that has param _x in the end
    regex_param = fr'{suffix}[0-9]+{parameter_prefix}$'
    cells_with_param = [s for s in columns if re.match(regex_param, s)]
    # remove the prefix from the cells, which gives us the name of cells
    regex_without_param = fr'{suffix}[0-9]+'
    cells_names = list(map(lambda a:
                           re.findall(regex_without_param, a)[0],
                           cells_with_param))

    return cells_names


def get_side_effect_columns(columns):
    """
    Retrieves the list of side effect cells' names
    """

    suffix = "L"

    # first remove the columns that does not represent cells
    #  or have parameter in the end
    regex_cells_only = fr'{suffix}[0-9]+$'
    cells_only = [s for s in columns if re.match(regex_cells_only, s)]

    # get no side effect cells
    no_side_effect_cells = get_cells_columns(columns=columns)
    # get side effect cells which does not have parameter
    #  prefix (in this case prefix =_x)
    side_effects = list(set(cells_only) - set(no_side_effect_cells))

    return side_effects


def calculate_correlation(matrix, columns):
    """calculate columns correlation matrix"""
    # check if columns belongs to the matrix
    is_columns_included = validator.is_columns_in_matrix(
        matrix=matrix, columns=columns)
    # if columns does not belong to the matrix, raise
    if not is_columns_included:
        raise ValueError(
            NOT_INCLUDED_ERROR_MSG)
    # if columns are empty return empty matrix
    if len(columns) == 0:
        return Matrix(matrix=[], columns=[])
    pandas_calculations = PandasCalculations()
    calculation_handler = CalculationsHandler(pandas_calculations)
    correlation = calculation_handler.correlation(matrix, columns)
    return correlation


def calculate_regression(matrix, columns):
    """calculate regression"""
    # check if columns belongs to the matrix
    is_columns_included = validator.is_columns_in_matrix(
        matrix=matrix, columns=columns)
    # if columns does not belong to the matrix, raise
    if not is_columns_included:
        raise ValueError(NOT_INCLUDED_ERROR_MSG)
    # if columns length different than 2 raise exception
    # it is a mandatory to specify only two columns'
    # because it is not multiple regression
    if len(columns) != 2:
        raise ValueError("Number of columns to calculate regression must be 2")
    pandas_operations = PandasOperations()
    operations_handler = OperationsHandler(pandas_operations)
    # take only the columns we need from the matrix
    reduced_matrix = operations_handler.drop_columns_except(matrix, columns)
    # scale the matrix between -1 and 1s
    matrix_scaled = operations_handler.scale_matrix(reduced_matrix)
    pandas_calculations = PandasCalculations()
    # calculate linear regression coefficients a and b
    calculation_handler = CalculationsHandler(pandas_calculations)
    regression_coef = calculation_handler.regression(matrix_scaled)

    return regression_coef, matrix_scaled


def merge_columns(matrix, columns_to_merge, new_column_name):
    """merge columns in columns_to_merge into new_column_name"""
    # check if columns_to_merge belongs to the matrix
    is_columns_included = validator.is_columns_in_matrix(
        matrix=matrix, columns=columns_to_merge)
    # if columns_to_merge does not belong to the matrix, raise
    if not is_columns_included:
        raise ValueError(NOT_INCLUDED_ERROR_MSG)
    # if columns_to_merge is empty raise exception
    if len(columns_to_merge) == 0:
        raise ValueError("number of columns to merge must be greater than 0")
    pandas_operations = PandasOperations()
    operations_handler = OperationsHandler(pandas_operations)
    merged_matrix = operations_handler.merge_columns_average(
        matrix, columns_to_merge, new_column_name)

    return merged_matrix


def group_matrix_by_column(matrix, columns_to_group):
    """group matrix by column"""
    # check if columns_to_group belongs to the matrix
    is_columns_included = validator.is_columns_in_matrix(
        matrix=matrix, columns=columns_to_group)
    # if columns_to_group does not belong to the matrix, raise
    if not is_columns_included:
        raise ValueError(NOT_INCLUDED_ERROR_MSG)
    # if columns_to_group is empty raise exception
    if len(columns_to_group) == 0:
        raise ValueError("number of columns to group must be greater than 0")
    pandas_operations = PandasOperations()
    operations_handler = OperationsHandler(pandas_operations)
    grouped_matrix = operations_handler.group_by_column(
        matrix, columns_to_group)

    return grouped_matrix


def filter_matrix_min_max(matrix, column_name, min_value, max_value):
    """"""
    # check if column_name exists in matrix's columns
    if column_name not in matrix.columns:
        raise ValueError(f"{column_name} does not exist in the matrix")

    pandas_operations = PandasOperations()
    operations_handler = OperationsHandler(pandas_operations)
    filtered_matrix = operations_handler.filter_min_max(
        matrix, column_name, min_value, max_value)

    return filtered_matrix


def convert_matrix_to_series(matrix, column_x, column_y, column_values):
    """convert matrix object to series needed by front-end client"""
    # check if columns exist in matrix's columns
    ordered_matrix_columns = sorted(matrix.columns)
    ordered_columns = sorted([column_x, column_y, column_values])
    is_columns_exist_in_matrix = set(ordered_columns).issubset(
        set(ordered_matrix_columns))
    if not is_columns_exist_in_matrix:
        raise ValueError(
            "one of the specified columns does not exist in the matrix")
    return formatter.convert_matrix_to_series(matrix,
                                              column_x, column_y,
                                              column_values)
