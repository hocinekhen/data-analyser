from django.test import TestCase, Client

from ..controller import get_matrix_from_file, get_matrix_object, get_matrix, \
    get_cells_columns, get_side_effect_columns, \
    calculate_correlation, calculate_regression, \
    merge_columns, group_matrix_by_column, \
    filter_matrix_min_max, convert_matrix_to_series
from ..helpers import exceptions
from ..helpers.matrix_helper import Matrix


class TestViews(TestCase):

    def SetUp(self):
        self.client = Client()

    def test_get_matrix_from_file(self):
        expected = Matrix(matrix=[[12, 14], [10, 15]],
                          columns=["column1", "column2"])
        result = get_matrix_from_file("test_not_remove.csv")
        self.assertEquals(result, expected)

    def test_get_matrix_from_file_no_file(self):
        self.assertRaises(exceptions.ValidationError,
                          get_matrix_from_file, 'file_not_exist.csv')

    def test_get_matrix_object(self):
        matrix = [[14, 12, 14], [55, 66, 43]]
        columns = ["column1", "column2", "coylumn3"]
        expected = Matrix(matrix=matrix, columns=columns)
        result = get_matrix_object(matrix=matrix, columns=columns)
        self.assertEquals(result, expected)

    def test_get_matrix_object_columns_length_not_equal(self):
        matrix = [[14, 12, 14], [55, 66, 43]]
        columns = ["column1", "column2", "coylumn3", "dk"]
        self.assertRaises(ValueError, get_matrix_object,
                          matrix=matrix, columns=columns)

    def test_get_matrix_from_body(self):
        columns = ["columnx", "columny", "columnz"]
        matrix = [[12, 13, 44], [22, 44, 6]]
        expected = Matrix(matrix=matrix, columns=columns)
        body = {
            "is_in_body": True,
            "matrix": {
                "matrix": [[12, 13, 44], [22, 44, 6]],
                "columns": ["columnx", "columny", "columnz"]
            }
        }

        result = get_matrix(body=body)
        self.assertEquals(result, expected)

    def test_get_matrix_bring_from_file(self):
        file_name = "test_not_remove.csv"
        expected = Matrix(matrix=[[12, 14], [10, 15]],
                          columns=["column1", "column2"])
        body = {
            "is_in_body": False
        }

        result = get_matrix(body=body, file_name=file_name)
        self.assertEquals(result, expected)

    def test_get_matrix_wrong_columns_length(self):
        body = {
            "is_in_body": True,
            "matrix": {
                "matrix": [[12, 13, 44], [22, 44, 6]],
                "columns": ["columnx", "columny", "columnz", "extra_column"]
            }
        }

        self.assertRaises(ValueError, get_matrix, body=body)

    def test_get_cells_columns(self):
        columns = ["L5424_x", "L6658_x", "L5424", "L6658", "L777", "L888"]
        expected = ["L5424", "L6658"]
        result = get_cells_columns(columns=columns)
        self.assertListEqual(sorted(result), sorted(expected))

    def test_get_cells_columns_wrong_parameter(self):
        columns = ["L5424_x", "L6658_YY", "L5424", "L6658", "L777", "L888"]
        expected = ["L5424"]
        result = get_cells_columns(columns=columns)
        self.assertEquals(sorted(result), sorted(expected))

    def test_get_cells_columns_empty_columns(self):
        columns = []
        expected = []
        result = get_cells_columns(columns=columns)
        self.assertEquals(sorted(result), sorted(expected))

    def test_get_side_effect_columns(self):
        columns = ["L5424_x", "L6658_x", "L5424", "L6658", "L777", "L888"]
        expected = ["L777", "L888"]
        result = get_side_effect_columns(columns=columns)
        self.assertEquals(sorted(result), sorted(expected))

    def test_get_side_effect_columns_wrong_parameter(self):
        columns = ["L5424_x", "L6658_YY", "L5424", "L6658", "L777", "L888"]
        expected = ["L777", "L888", "L6658"]
        result = get_side_effect_columns(columns=columns)
        self.assertEquals(sorted(result), sorted(expected))

    def test_get_side_effect_columns_empty_columns(self):
        columns = []
        expected = []
        result = get_side_effect_columns(columns=columns)
        self.assertEquals(sorted(result), sorted(expected))

    def test_calculate_correlation(self):
        matrix = Matrix(matrix=[[12, 14], [10, 15], [3, 14], [10, 20], [
            12, 5], [30, 10]], columns=["column1", "column2"])
        columns = ["column1", "column2"]
        expected = Matrix(matrix=[[1, -0.3541], [-0.3541, 1]],
                          columns=["column1", "column2"])

        result = calculate_correlation(matrix=matrix, columns=columns)
        self.assertEquals(result, expected)

    def test_calculate_correlation_not_all_columns(self):
        matrix = Matrix(matrix=[[12, 14], [10, 15], [3, 14], [10, 20], [
            12, 5], [30, 10]], columns=["column1", "column2"])
        columns = ["column1"]
        expected = Matrix(matrix=[[1]], columns=["column1"])

        result = calculate_correlation(matrix=matrix, columns=columns)
        self.assertEquals(result, expected)
        self.assertEquals(sorted(result.columns), sorted(columns))

    def test_calculate_correlation_empty_columns(self):
        matrix = Matrix(matrix=[[12, 14], [10, 15], [3, 14], [10, 20], [
            12, 5], [30, 10]], columns=["column1", "column2"])
        columns = []
        expected = Matrix(matrix=[], columns=[])

        result = calculate_correlation(matrix=matrix, columns=columns)
        self.assertEquals(result, expected)
        self.assertEquals(sorted(result.columns), sorted(columns))

    def test_calculate_correlation_columns_not_in_matrix(self):
        matrix = Matrix(matrix=[[12, 14], [10, 15], [3, 14], [10, 20], [
            12, 5], [30, 10]], columns=["column1", "column2"])
        columns = ["not_in_matrix"]

        self.assertRaises(ValueError, calculate_correlation,
                          matrix=matrix, columns=columns)

    def test_calculate_regression(self):
        matrix = Matrix(matrix=[[12, 14], [10, 15], [3, 14], [
            10, 20]], columns=["column1", "column2"])
        columns = ["column1", "column2"]
        expected = Matrix(matrix=[[1, 0], [0.7778, 0.1667], [0, 0], [
            0.7778, 1]], columns=["column1", "column2"])

        coefficients, scaled_matrix = calculate_regression(
            matrix=matrix, columns=columns)
        expected_coffiecient = {'a': 0.2808, 'b': 0.1123}
        self.assertEquals(scaled_matrix, expected)
        self.assertEquals(coefficients, expected_coffiecient)

    def test_calculate_regression_one_column(self):
        matrix = Matrix(matrix=[[12, 14], [10, 15], [3, 14], [
            10, 20]], columns=["column1", "column2"])
        columns = ["column1"]

        self.assertRaises(ValueError, calculate_regression,
                          matrix=matrix, columns=columns)

    def test_calculate_regression_columns_not_in_matrix(self):
        matrix = Matrix(matrix=[[12, 14], [10, 15], [3, 14], [
            10, 20]], columns=["column1", "column2"])
        columns = ["column1", "dkfj"]

        self.assertRaises(ValueError, calculate_regression,
                          matrix=matrix, columns=columns)

    def test_merge_columns(self):
        matrix = Matrix(matrix=[[12, 14, 32], [10, 15, 4],
                                [3, 14, 4], [10, 20, 32]],
                        columns=["column1", "column2", "column3"])
        columns_to_merge = ["column2", "column3"]
        new_column_name = "new_column"
        expected = Matrix(matrix=[[12, 23], [10, 9.5], [3, 9], [
            10, 26]], columns=["column1", "new_column"])

        result = merge_columns(matrix=matrix,
                               columns_to_merge=columns_to_merge,
                               new_column_name=new_column_name)

        self.assertEquals(result, expected)

    def test_merge_columns_not_in_matrix(self):
        matrix = Matrix(matrix=[[12, 14, 32], [10, 15, 4],
                                [3, 14, 4], [10, 20, 32]],
                        columns=["column1", "column2", "column3"])
        columns_to_merge = ["column2", "not_in_matrix"]
        new_column = "new_column"
        self.assertRaises(ValueError, merge_columns,
                          matrix=matrix, columns_to_merge=columns_to_merge,
                          new_column_name=new_column)

    def test__merge_columns_empty_columns(self):
        matrix = Matrix(matrix=[[12, 14, 32], [10, 15, 4],
                                [3, 14, 4], [10, 20, 32]],
                        columns=["column1", "column2", "column3"])
        columns_to_merge = []
        new_column = "new_column"
        self.assertRaises(ValueError, merge_columns,
                          matrix=matrix, columns_to_merge=columns_to_merge,
                          new_column_name=new_column)

    def test_group_columns(self):
        matrix = Matrix(matrix=[[12, 14, 32], [12, 14, 4],
                                [12, 14, 4], [12, 20, 30]],
                        columns=["column1", "column2", "column3"])
        columns_to_group = ["column1", "column2"]
        expected = Matrix(matrix=[[12, 14, 13.3333], [12, 20, 30]], columns=[
            "column1", "column2", "column3"])

        result = group_matrix_by_column(
            matrix=matrix, columns_to_group=columns_to_group)
        self.assertEquals(result, expected)

    def test_group_columns_not_in_matrix(self):
        matrix = Matrix(matrix=[[12, 14, 32], [12, 14, 4],
                                [12, 14, 4], [12, 20, 30]],
                        columns=["column1", "column2", "column3"])
        columns_to_group = ["column2", "not_in_matrix"]

        self.assertRaises(ValueError, group_matrix_by_column,
                          matrix=matrix, columns_to_group=columns_to_group)

    def test_group_columns_empty_columns(self):
        matrix = Matrix(matrix=[[12, 14, 32], [12, 14, 4],
                                [12, 14, 4], [12, 20, 30]],
                        columns=["column1", "column2", "column3"])
        columns_to_group = []

        self.assertRaises(ValueError, group_matrix_by_column,
                          matrix=matrix, columns_to_group=columns_to_group)

    def test_filter_min_max(self):
        matrix = Matrix(matrix=[[1, 2, 32], [2, 14, 4], [3, 14, 4], [
            4, 20, 30]], columns=["column1", "column2", "column3"])
        column_name = "column1"
        min_ = 2
        max_ = 3
        expected = Matrix(matrix=[[2, 14, 4], [3, 14, 4]],
                          columns=["column1", "column2", "column3"])

        result = filter_matrix_min_max(matrix=matrix, column_name=column_name,
                                       min_value=min_, max_value=max_)
        self.assertEquals(result, expected)

    def test_filter_min_max_column_not_in_matrix(self):
        matrix = Matrix(matrix=[[1, 2, 32], [2, 14, 4], [3, 14, 4], [
            4, 20, 30]], columns=["column1", "column2", "column3"])
        column_name = "not_in_matrix"
        min_ = 2
        max_ = 3

        self.assertRaises(ValueError, filter_matrix_min_max, matrix=matrix,
                          column_name=column_name,
                          min_value=min_, max_value=max_)

    def test_convert_matrix_to_series(self):
        matrix = Matrix(matrix=[[1, 2, 32], [2, 14, 4], [3, 14, 4]], columns=[
            "column1", "column2", "column3"])
        column_x = "column1"
        column_y = "column2"
        column_values = "column3"
        expected = {
            'axis_x': [1, 2, 3],
            'axis_y': [
                {'name': 2, 'data': [32.0, 0, 0]},
                {'name': 14, 'data': [0, 4.0, 4.0]}
            ],
            'groups': [2, 14]
        }

        result = convert_matrix_to_series(
            matrix, column_x, column_y, column_values)
        self.assertEquals(result, expected)

    def test_convert_matrix_to_series_columns_not_in_matrix(self):
        matrix = Matrix(matrix=[[1, 2, 32], [2, 14, 4], [3, 14, 4]], columns=[
            "column2", "column1", "column3"])
        column_x = "column1"
        column_y = "column2"
        column_values = "not_in_matrix"

        self.assertRaises(ValueError, convert_matrix_to_series,
                          matrix, column_x, column_y, column_values)
