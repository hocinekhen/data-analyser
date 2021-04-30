import json

from django.test import TestCase, Client
from django.urls import reverse

CSV_FILE_NAME = 'file.csv'
CONTENT_TYPE = "application/json"


class TestViews(TestCase):

    def SetUp(self):
        self.client = Client()

    def test_matrix_GET(self):
        url = 'matrix'
        response = self.client.get(reverse(url, args=['test_not_remove.csv']))
        self.assertEquals(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEquals(response_json["data"]["_Matrix__columns"], [
                          "column1", "column2"])

    def test_matrix_no_existing_file_GET(self):
        url = 'matrix'
        response = self.client.get(
            reverse(url, args=['file_does_not_exist.csv']))

        self.assertEquals(response.status_code, 400)

    def test_columns_GET(self):
        url = 'columns'
        response = self.client.get(reverse(url, args=['test_not_remove.csv']))
        self.assertEquals(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEquals(response_json["data"], ["column1", "column2"])

    def test_columns_no_existing_file_GET(self):
        url = 'columns'
        response = self.client.get(
            reverse(url, args=['file_does_not_exist.csv']))

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)

    # cells
    def test_cells_Post(self):
        url = 'cells'
        body = {
            "columns": ["L5424_x", "L6658_x", "L5424", "L6658", "L777", "L888"]
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)
        self.assertEquals(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], False)
        self.assertEquals(
            sorted(response_json["data"]), sorted(["L5424", "L6658"]))

    def test_cells_invalid_body_POST(self):
        url = 'cells'
        body = {}
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)

    # side_effect cells
    def test_side_effects_Post(self):
        url = 'side_effect'
        body = {
            "columns": ["L5424_x", "L6658_x", "L5424", "L6658", "L777", "L888"]
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)
        self.assertEquals(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], False)
        response_json = json.loads(response.content)
        self.assertEquals(
            sorted(response_json["data"]), sorted(["L777", "L888"]))

    def test_side_effects_invalid_body_POST(self):
        url = 'side_effect'
        body = {}
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)

    # Correlation
    def test_correlation_Post(self):
        url = 'correlation'
        body = {
            "columns": [
                "a",
                "b"
            ],
            "is_in_body": True,
            "matrix": {
                "matrix": [[1, 2], [2, 2], [3, 4], [4, 5]],
                "columns": ["a", "b"]
            }
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)
        self.assertEquals(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], False)
        expected_matrix = [[1.0, 0.9467], [0.9467, 1.0]]
        self.assertEquals(response_json["data"]
                          ["_Matrix__matrix"], expected_matrix)

    def test_correlation_column_not_in_matrix_POST(self):
        url = 'correlation'
        body = {
            "columns": [
                "other_column",
                "b"
            ],
            "is_in_body": True,
            "matrix": {
                "matrix": [[1, 2], [2, 2], [3, 4], [4, 5]],
                "columns": ["a", "b"]
            }
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)

    def test_correlation_invalid_body_POST(self):
        url = 'correlation'
        body = {
            "columns": [
                "a",
                "b"
            ],
            "is_in_body": True,
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)

    # Regression
    def test_regression_Post(self):
        url = 'regression'
        body = {
            "columns": [
                "a",
                "b"
            ],
            "is_in_body": True,
            "matrix": {
                "matrix": [[1, 2], [2, 2], [3, 4], [4, 5]],
                "columns": ["a", "b"]
            }
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)
        self.assertEquals(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], False)

    def test_regression_one_column_POST(self):
        url = 'regression'
        body = {
            "columns": [
                "a"
            ],
            "is_in_body": True,
            "matrix": {
                "matrix": [[1, 2], [2, 2], [3, 4], [4, 5]],
                "columns": ["a", "b"]
            }
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)

    def test_regression_invalid_body_POST(self):
        url = 'regression'
        body = {
            "field": [
                "a",
                "b"
            ],
            "is_in_body": True,
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)

    # Merging
    def test_merge_Post(self):
        url = 'merge'
        body = {
            "columns_to_merge": [
                "a",
                "b"
            ],
            "column_name": "merged_column",
            "is_in_body": True,
            "matrix": {
                "matrix": [[1, 2, 3], [2, 2, 4], [3, 4, 7], [4, 5, 8]],
                "columns": ["a", "b", "c"]
            }
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)
        self.assertEquals(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], False)
        expected_matrix = [[3.0, 1.5], [4.0, 2.0], [7.0, 3.5], [8.0, 4.5]]
        self.assertEquals(response_json["data"]
                          ["_Matrix__matrix"], expected_matrix)

    def test_merge_invalid_body_POST(self):
        url = 'merge'
        body = {
            "columns": [
                "a",
                "b"
            ],
            "is_in_body": True,
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)

    # Grouping
    def test_group_Post(self):
        url = 'group'
        body = {
            "columns_to_group": [
                "b"
            ],
            "is_in_body": True,
            "matrix": {
                "matrix": [[1, 2], [2, 2], [1, 4], [4, 5]],
                "columns": ["a", "b"]
            }
        }

        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)
        self.assertEquals(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], False)
        expected_matrix = [[2.0, 1.5], [4.0, 1.0], [5.0, 4.0]]
        self.assertEquals(response_json["data"]
                          ["_Matrix__matrix"], expected_matrix)

    def test_group_all_columns_body_POST(self):
        url = 'group'
        body = {
            "columns_to_group": [
                "a",
                "b"
            ],
            "is_in_body": True,
            "matrix": {
                "matrix": [[1, 2], [2, 2], [3, 4], [4, 5]],
                "columns": ["a", "b"]
            }
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)

    def test_group_invalid_body_POST(self):
        url = 'group'
        body = {
            "columns": [
                "a",
                "b"
            ],
            "is_in_body": True,
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)

    def test_group_column_not_in_matrix_POST(self):
        url = 'group'
        body = {
            "columns_to_group": [
                "a",
                "other_field"
            ],
            "is_in_body": True,
            "matrix": {
                "matrix": [[1, 2], [2, 2], [3, 4], [4, 5]],
                "columns": ["a", "b"]
            }
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)

    # Filtering
    def test_filter_Post(self):
        url = 'filter'
        body = {
            "column_to_filter": "a",
            "min": 1,
            "max": 2,
            "is_in_body": True,
            "matrix": {
                "matrix": [[1, 2], [2, 2], [3, 4], [4, 5]],
                "columns": ["a", "b"]
            }
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)
        self.assertEquals(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], False)
        expected_matrix = [[1, 2], [2, 2]]
        self.assertEquals(response_json["data"]
                          ["_Matrix__matrix"], expected_matrix)

    def test_filter_invalid_body_POST(self):
        url = 'filter'
        body = {
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)

    def test_filter_column_not_in_matrix_POST(self):
        url = 'filter'
        body = {
            "column_to_filter": "other_column",
            "min": 1,
            "max": 2,
            "is_in_body": True,
            "matrix": {
                "matrix": [[1, 2], [2, 2], [3, 4], [4, 5]],
                "columns": ["a", "b"]
            }
        }
        response = self.client.post(reverse(url, args=[CSV_FILE_NAME]),
                                    json.dumps(body),
                                    content_type=CONTENT_TYPE)

        self.assertEquals(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['error'], True)
