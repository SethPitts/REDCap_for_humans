import csv
import json
from collections import OrderedDict


def get_generic_headers(file_data: list):
    """
    Create generic headers for files that don't contain headers
    :param file_data: list containing the data from the file
    :return: list of generic headers to use with the file
    """
    generic_headers = ['col_{}'.format(row_num)
                       for row_num, _ in file_data
                       ]
    return generic_headers


def get_text_data(data_file_path: str, headers: bool, delimiter=' ') -> OrderedDict:
    """
    Get data from a .txt file
    :param data_file_path: pathway to file
    :param headers: True if file contains headers, False if file does not contain headers
    :param delimiter: delimiter that separates the data in the text file. Defaults to space
    :return: OrderedDict containing the file data
    """
    file_data = OrderedDict()
    if headers is True:
        with open(data_file_path, 'r') as text_file:
            file_data['headers'] = text_file.readline().replace('\n', '').split(delimiter)  # Assume headers are first line of file
            for row_num, line in enumerate(text_file):
                file_data[row_num] = line.replace('\n', '').split(delimiter)

            return file_data

    if headers is False:
        with open(data_file_path, 'r') as text_file:
            text_data = [line.replace('\n', '').split(delimiter)
                         for line in text_file
                         ]
            file_data['headers'] = get_generic_headers(text_data)
            for row_num, row in enumerate(text_data):
                file_data[row_num] = row

            return file_data


def get_csv_data(data_file_path: str, headers: bool):
    """
    Get data from a .csv file
    :param data_file_path: pathway to file
    :param headers: True if file contains headers, False if file does not contain headers
    :return: OrderedDict containing the file data
    """
    file_data = OrderedDict()
    if headers is True:
        with open(data_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            file_data['headers'] = csv_reader.fieldnames
            for row_num, row in enumerate(csv_reader):
                file_data[row_num] = row

            return file_data

    if headers is False:
        with open(data_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            csv_data = list(csv_reader)
            file_data['headers'] = get_generic_headers(csv_data)
            for row_num, row in enumerate(csv_data):
                file_data[row_num] = row

            return file_data


def get_tsv_data(data_file_path: str, headers: bool):
    """
    Get data from a .tsv file
    :param data_file_path: pathway to file
    :param headers: True if file contains headers, False if file does not contain headers
    :return: OrderedDict containing the file data
    """
    file_data = OrderedDict()
    if headers is True:
        with open(data_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='\t')
            file_data['headers'] = csv_reader.fieldnames
            for row_num, row in enumerate(csv_reader):
                file_data[row_num] = row

            return file_data

    if headers is False:
        with open(data_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            csv_data = list(csv_reader)
            file_data['headers'] = get_generic_headers(csv_data)
            for row_num, row in enumerate(csv_data):
                file_data[row_num] = row

            return file_data


def get_json_data(data_file_path: str, headers: bool):
    """
    Get data from a .json file
    :param data_file_path: pathway to file
    :param headers: True if file contains headers, False if file does not contain headers
    :return: OrderedDict containing the file data
    """

    # TODO: Flatten out the json file by created list of headers to call each value of the json object
    # TODO: Use those headers to make calls to the json data
    file_data = OrderedDict()
    if headers is True:
        with open(data_file_path, 'r') as json_file:
            json_data = json.load(json_file, object_pairs_hook=OrderedDict)
            # Get headers
            if type(json_data) == list:
                file_data['headers'] = json_data[0].keys()
                for row_num, row in enumerate(json_data):
                    file_data[row_num] = row
                return file_data

            if type(json_data) == OrderedDict:
                json_base_objects = list(json_data.keys())
                for header in json_base_objects:
                    file_data['{}_headers'.format(header)] = json_data[header][0].keys()
                    for row_num, row in enumerate(json_data[header]):
                        file_data['{}_{}'.format(header, row_num)] = row
                return file_data


def recursive_json_header(json_data, headers=None, header_to_add=None):
    print(headers)
    if headers is None:
        headers = []
    if type(json_data) not in (list, OrderedDict) or json_data == []:
        print("base ran")
        print("appending {}".format(header_to_add))
        headers.append(header_to_add)
        return headers
    if type(json_data) == list:
        print("list ran")
        if type(json_data[0]) not in (list, OrderedDict):
            print("appending {}".format(header_to_add))
            headers.append(header_to_add)
        else:
            recursive_json_header(json_data[0], headers)
    if type(json_data) == OrderedDict:
        print("dict ran")
        possible_headers = json_data.keys()
        for possible_header in possible_headers:
            recursive_json_header(json_data[possible_header], headers, possible_header)

def main():
    with open('test3.json', 'r') as json_file:
        json_data = json.load(json_file, object_pairs_hook=OrderedDict)
        headers = recursive_json_header(json_data)
    print(headers)


if __name__ == '__main__':
    main()
