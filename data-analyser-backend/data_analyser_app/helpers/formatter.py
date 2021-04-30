"""Contains functionalities
related to display and handle output format
needed by the client side"""

import pandas as pd


def convert_matrix_to_series(matrix, column_x, column_y, column_values):
    """
    convert a matrix to a series format
    needed by the front-end client for bar chart

    Parameters
    ----------
    matrix : Matrix
        the matrix we want to convert
    column_x : string
        The column that will be used in the x axis of the bar chart
    column_y : string
        The column that will be used in the y axis of the bar chart
    column_values : string
        The column that will be used to retrieve the values
         of the corresponding line in the matrix
         indexed by (column_x, column_y)

    Returns
    -------
    example:
        {
            axis_x=['day1','day2','day3'],
            groups=['26']
            axis_y = [
                {
                    "name":"26",
                    "data":[15,14,25]
                }
            ]
        }
    """
    dataframe = pd.DataFrame(data=matrix.matrix, columns=matrix.columns)
    grouped_matrix = dataframe.groupby([column_x, column_y])
    # get values of column_x without duplicats
    val_x = list(dataframe[column_x]
                 .drop_duplicates(keep="first"))
    # get values of column_y without duplicats
    val_y = list(dataframe[column_y]
                 .drop_duplicates(keep="first"))
    # sort
    val_x.sort()
    val_y.sort()
    # get the groups obtained from grouping the original matrix
    groups = list(grouped_matrix.groups.keys())
    series_list = []
    for y_element in val_y:
        new_serie = {"name": y_element, "data": []}
        for x_element in val_x:
            if (x_element, y_element) in groups:

                # add the corresponding value of the group
                # to the current serie's data
                value_to_append = float(grouped_matrix
                                        .get_group((x_element, y_element))
                                        .mean()[column_values])
                new_serie["data"] \
                    .append(value_to_append)
            else:
                # otherwise fill it with 0 value
                new_serie["data"].append(0)
        # add the new_serie to the list of series
        series_list.append(new_serie)
    return {
        "axis_x": val_x,
        "axis_y": series_list,
        "groups": val_y
    }
