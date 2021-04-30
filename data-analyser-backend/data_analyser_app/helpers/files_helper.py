"""Contains the functions related to manipulating csv files"""


import abc
import os

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

import pandas as pd

from .matrix_helper import Matrix


class PeristanceInterface(metaclass=abc.ABCMeta):
    """Interface responsible for different csv file storage operations"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'save_file') and
                callable(subclass.save_file) or
                NotImplemented)

    @abc.abstractmethod
    def save_file(self, data, file_name: str):
        """Save the data into a file in the local machine"""
        raise NotImplementedError


class FileSystemStoragePersistance(PeristanceInterface):
    """Handle storing file using FileSystemStorage"""

    def save_file(self, data: InMemoryUploadedFile, file_name: str):
        """Save the data into a file using FileSystemStorage"""
        fs = FileSystemStorage()
        filename = fs.save(file_name, data)

        return filename


class FileWriter():
    """Handle uploading file to the local machine"""

    def __init__(self, persistance):
        self._persistance = persistance

    def write_file(self, data: InMemoryUploadedFile, file_name: str):
        """store data into file"""
        filename = self._persistance.save_file(data, file_name)

        return filename


class Reader(metaclass=abc.ABCMeta):
    """Handle reading operations of the csv file and\
         converting it to different formats"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'csv_to_matrix') and
                callable(subclass.csv_to_matrix) or
                NotImplemented)

    @abc.abstractmethod
    def csv_to_matrix(self, path: str, file_name: str):
        """Reads a csv file and convert it to Matrix object"""
        raise NotImplementedError


def get_csv_separator():
    """
    Temporary function to retrieve separator of
    a given file
    """
    # TODO: This can be retrieved from database in the future
    return ";"


class PandasReader(Reader):
    """Handle Reading csv files using Pandas"""

    def csv_to_matrix(self, path: str, file_name: str):
        """convert csv file to matrix object"""
        csv_file_path = os.path.join(path, file_name)
        csv_separator = get_csv_separator()
        dataframe = pd.read_csv(csv_file_path, header=0, sep=csv_separator)
        # make sure floats are separated by '.' and not ','
        dataframe.replace(',', '.', inplace=True, regex=True)
        # convert to float
        dataframe = dataframe.astype(float)
        columns = dataframe.columns.values
        matrix = Matrix(dataframe.to_numpy(), columns)
        return matrix


class FileReader():
    """Handle reading the csv file and retrieve the Matrix object"""

    def __init__(self, reader):
        self._reader = reader

    def csv_to_matrix(self, path: str, file_name: str):
        """Convert data in csv file to matrix object"""
        # implement any data processing here ex. parsing

        # get matrix object from csv
        matrix = self._reader.csv_to_matrix(path, file_name)

        return matrix
