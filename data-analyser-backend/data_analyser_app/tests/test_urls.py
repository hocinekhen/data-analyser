from django.test import SimpleTestCase
from django.urls import reverse, resolve

from data_analyser_app.views import upload, get_matrix, get_columns, \
    get_cells_columns, get_side_effect_columns, \
    calculate_correlation, merge_columns, group_matrix_by_columns, \
    filter_matrix_by_column, matrix_to_series, \
    calculate_regression

CSV_FILE_NAME = 'some-file.csv'


class TestUrls(SimpleTestCase):

    def test_upload_url_is_resolved(self):
        url = reverse('upload')
        self.assertEquals(resolve(url).func, upload)

    def test_matrix_url_is_resolved(self):
        url = reverse('matrix', args=[CSV_FILE_NAME])
        self.assertEquals(resolve(url).func, get_matrix)

    def test_columns_url_is_resolved(self):
        url = reverse('columns', args=[CSV_FILE_NAME])
        self.assertEquals(resolve(url).func, get_columns)

    def test_cells_url_is_resolved(self):
        url = reverse('cells', args=[CSV_FILE_NAME])
        self.assertEquals(resolve(url).func, get_cells_columns)

    def test_side_effect_url_is_resolved(self):
        url = reverse('side_effect', args=[CSV_FILE_NAME])
        self.assertEquals(resolve(url).func, get_side_effect_columns)

    def test_correlation_url_is_resolved(self):
        url = reverse('correlation', args=[CSV_FILE_NAME])
        self.assertEquals(resolve(url).func, calculate_correlation)

    def test_merge_url_is_resolved(self):
        url = reverse('merge', args=[CSV_FILE_NAME])
        self.assertEquals(resolve(url).func, merge_columns)

    def test_group_url_is_resolved(self):
        url = reverse('group', args=[CSV_FILE_NAME])
        self.assertEquals(resolve(url).func, group_matrix_by_columns)

    def test_filter_url_is_resolved(self):
        url = reverse('filter', args=[CSV_FILE_NAME])
        self.assertEquals(resolve(url).func, filter_matrix_by_column)

    def test_series_url_is_resolved(self):
        url = reverse('series', args=[CSV_FILE_NAME])
        self.assertEquals(resolve(url).func, matrix_to_series)

    def test_regression_url_is_resolved(self):
        url = reverse('regression', args=[CSV_FILE_NAME])
        self.assertEquals(resolve(url).func, calculate_regression)
