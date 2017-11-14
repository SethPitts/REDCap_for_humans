import csv
from collections import OrderedDict


def get_generic_headers(file_data: list):
    generic_headers = ['col_{}'.format(row_num)
                       for row_num, _ in file_data
                       ]
    return generic_headers


def get_text_data(data_file_path: str, headers: bool):
    file_data = OrderedDict()
    if headers is True:
        with open(data_file_path, 'r') as text_file:
            file_data['headers'] = text_file.read().replace('\n', '')  # Assume headers are first line of file
            for row_num, line in enumerate(text_file):
                file_data[row_num] = line.replace('\n', '')

            return file_data

    if headers is False:
        with open(data_file_path, 'r') as text_file:
            text_data = [line.replace('\n', '')
                         for line in text_file
                         ]
            file_data['headers'] = get_generic_headers(text_data)
            for row_num, row in enumerate(text_data):
                file_data[row_num] = row.replace('\n', '')

            return file_data


def get_csv_data(data_file_pathway: str, headers: bool):
    file_data = OrderedDict()
    if headers is True:
        with open(data_file_pathway, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            file_data['headers'] = csv_reader.fieldnames
            for row_num, row in enumerate(csv_reader):
                file_data[row_num] = row

            return file_data

    if headers is False:
        with open(data_file_pathway, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            csv_data = list(csv_reader)
            file_data['headers'] = get_generic_headers(csv_data)
            for row_num, row in enumerate(csv_data):
                file_data[row_num] = row

            return file_data
