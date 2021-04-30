from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# controller
from . import controller
from .helpers import exceptions
from .helpers import validator


def response_object_generator(data, is_error, message, status_code):
    """Builds Response object based on the parameters passed to it"""
    res = {"error": is_error, "message": message, "data": data}
    return Response(res, status=status_code)


@api_view(['GET'])
def get_matrix(request, file_name):
    try:
        matrix = controller.get_matrix_from_file(file_name)
        return response_object_generator(data=matrix.__dict__,
                                         is_error=False, message="",
                                         status_code=status.HTTP_200_OK)
    except exceptions.ValidationError as e:
        return response_object_generator(data=None,
                                         is_error=True, message=e.message,
                                         status_code=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_columns(request, file_name):
    """get all columns of the matrix"""
    try:
        matrix = controller.get_matrix_from_file(file_name)
        return response_object_generator(data=matrix.columns,
                                         is_error=False, message="",
                                         status_code=status.HTTP_200_OK)
    except exceptions.ValidationError as e:
        return response_object_generator(data=None,
                                         is_error=True, message=e.message,
                                         status_code=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_cells_columns(request, file_name):
    """
    Returns all the cells except the side effect cells
    """
    request_body = request.data
    # validate inputs
    try:
        # call needed validations here
        # if a validation fails it will raise ValidationError
        required_fields = ["columns"]
        validator.check_fields_presence(request_body=request_body,
                                        fields=required_fields)

        # list of columns from where we want
        # to retrieve the candidats's columns
        columns = request_body['columns']

        data = controller.get_cells_columns(columns)
        return response_object_generator(data=data,
                                         is_error=False, message="",
                                         status_code=status.HTTP_200_OK)
    except exceptions.ValidationError as e:
        # if you are here than it is an error of wrong inputs from the users
        # send 400 error code
        return response_object_generator(data=None,
                                         is_error=True, message=e.message,
                                         status_code=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_side_effect_columns(request, file_name):
    """
    side effect cells are referred to those cells that has not a
    parameter _x in the columns list
    """

    request_body = request.data
    # validate inputs
    try:
        # call needed validations here
        # if a validation fails it will raise ValidationError
        required_fields = ["columns"]
        validator.check_fields_presence(request_body=request_body,
                                        fields=required_fields)
        # list of columns from where we want
        # to retrieve the side effects' columns
        columns = request_body['columns']

        candidates = controller.get_side_effect_columns(columns)
        return response_object_generator(data=candidates,
                                         is_error=False, message="",
                                         status_code=status.HTTP_200_OK)
    except exceptions.ValidationError as e:
        return response_object_generator(data=None,
                                         is_error=True,
                                         message=e.message,
                                         status_code=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def calculate_correlation(request, file_name):
    request_body = request.data
    # validate inputs
    try:
        # call needed validations here
        # if a validation fails it will raise ValidationError

        validator.validate_correlation_body(request_body=request_body)
        columns = request_body['columns']
        matrix = controller.get_matrix(request_body, file_name)
        validator.check_if_columns_belong_to_matrix(matrix=matrix,
                                                    columns=columns)
        # calculate correlation
        correlation_matrix = controller.calculate_correlation(matrix, columns)

        return response_object_generator(data=correlation_matrix.__dict__,
                                         is_error=False, message="",
                                         status_code=status.HTTP_200_OK)
    except exceptions.ValidationError as e:
        return response_object_generator(data=None,
                                         is_error=True,
                                         message=e.message,
                                         status_code=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def calculate_regression(request, file_name):
    request_body = request.data
    # validate inputs
    try:
        # call needed validations here
        # if a validation fails it will raise ValidationError

        validator.validate_regression_body(request_body=request_body)
        columns = request_body['columns']
        matrix = controller.get_matrix(request_body, file_name)
        validator.check_if_columns_belong_to_matrix(matrix=matrix,
                                                    columns=columns)

        regression_coefficients, scaled_matrix = controller.calculate_regression(
            matrix, columns)
        data = scaled_matrix.__dict__
        data["regression_coeff"] = regression_coefficients
        return response_object_generator(data=data,
                                         is_error=False, message="",
                                         status_code=status.HTTP_200_OK)
    except exceptions.ValidationError as e:
        return response_object_generator(data=None,
                                         is_error=True,
                                         message=e.message,
                                         status_code=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def merge_columns(request, file_name):
    request_body = request.data
    # validate inputs
    try:
        # call needed validations here
        # if a validation fails it will raise ValidationError
        validator.validate_merge_body(request_body=request_body)
        columns_to_merge = request_body['columns_to_merge']
        # the name of the new column that will be obtained from merging
        new_column_name = request_body["column_name"]
        matrix = controller.get_matrix(request_body, file_name)
        # check if columns_to_merge are included in the matrix columns
        validator.check_if_columns_belong_to_matrix(
            matrix=matrix, columns=columns_to_merge)
        # merge columns
        merged_matrix = controller.merge_columns(
            matrix, columns_to_merge, new_column_name)
        return response_object_generator(data=merged_matrix.__dict__,
                                         is_error=False, message="",
                                         status_code=status.HTTP_200_OK)
    except exceptions.ValidationError as e:
        return response_object_generator(data=None,
                                         is_error=True,
                                         message=e.message,
                                         status_code=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def group_matrix_by_columns(request, file_name):
    request_body = request.data
    # validate inputs
    try:
        # call needed validations here
        # if a validation fails it will raise ValidationError
        validator.validate_group_body(request_body=request_body)
        columns_to_group = request_body['columns_to_group']
        matrix = controller.get_matrix(request_body, file_name)
        # check if columns_to_group are included in the matrix columns
        validator.check_if_columns_belong_to_matrix(
            matrix=matrix, columns=columns_to_group)
        # check if columns_to_group does not includ all the matrix columns
        is_all_matrix_columns = len(matrix.columns) == len(columns_to_group)
        if is_all_matrix_columns:
            raise exceptions.ValidationError(
                message="grouping all the columns is not possible")
        # group columns
        grouped_matrix = controller.group_matrix_by_column(matrix,
                                                           columns_to_group)
        return response_object_generator(data=grouped_matrix.__dict__,
                                         is_error=False, message="",
                                         status_code=status.HTTP_200_OK)
    except exceptions.ValidationError as e:
        return response_object_generator(data=None,
                                         is_error=True,
                                         message=e.message,
                                         status_code=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def filter_matrix_by_column(request, file_name):
    request_body = request.data
    # validate inputs
    try:
        # call needed validations here
        # if a validation fails it will raise ValidationError
        validator.validate_filter_body(request_body=request_body)
        matrix = controller.get_matrix(request_body, file_name)
        column_to_filter = request_body['column_to_filter']
        min_value = request_body["min"]
        max_value = request_body["max"]
        # check if columns_to_group are included in the matrix columns
        validator.check_if_columns_belong_to_matrix(matrix=matrix,
                                                    columns=[column_to_filter])
        filtered_matrix = controller.filter_matrix_min_max(matrix,
                                                           column_to_filter,
                                                           min_value,
                                                           max_value)
        return response_object_generator(data=filtered_matrix.__dict__,
                                         is_error=False, message="",
                                         status_code=status.HTTP_200_OK)
    except exceptions.ValidationError as e:
        return response_object_generator(data=None,
                                         is_error=True,
                                         message=e.message,
                                         status_code=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def matrix_to_series(request, file_name):
    """Returns chart series needed for the client to vizualize"""
    request_body = request.data
    # validate inputs
    try:
        # call needed validations here
        # if a validation fails it will raise ValidationError
        validator.validate_matrix_to_series_body(request_body=request_body)
        matrix = controller.get_matrix(request_body, file_name)
        column_x = request_body['column_x']
        column_y = request_body["column_y"]
        column_values = request_body["column_values"]
        # check if all columns names are different
        validator.check_columns_uniqueness(columns=[column_x, column_y,
                                                    column_values])
        # check if columns_to_group are included in the matrix columns
        validator.check_if_columns_belong_to_matrix(matrix=matrix,
                                                    columns=[column_x,
                                                             column_y,
                                                             column_values])

        series = controller.convert_matrix_to_series(matrix, column_x,
                                                     column_y, column_values)
        return response_object_generator(data=series,
                                         is_error=False, message="",
                                         status_code=status.HTTP_200_OK)
    except exceptions.ValidationError as e:
        return response_object_generator(data=None,
                                         is_error=True,
                                         message=e.message,
                                         status_code=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def upload(request):
    """store the csv file uploaded by the user"""
    uploaded_file = request.FILES['file']
    if 'file' not in request.FILES:
        return response_object_generator(data=None,
                                         is_error=True,
                                         message="file is not present!",
                                         status_code=status.HTTP_400_BAD_REQUEST)
    file_name = controller.write_file(uploaded_file)
    return response_object_generator(data=file_name,
                                     is_error=False, message="",
                                     status_code=status.HTTP_200_OK)


@api_view(['GET'])
def test(request):
    return Response({'data': "api is working..."})
