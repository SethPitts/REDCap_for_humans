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
            file_data['headers'] = text_file.readline().replace('\n', '').split(
                delimiter)  # Assume headers are first line of file
            for row_num, line in enumerate(text_file):
                data = OrderedDict()
                for header, value in zip(file_data['headers'], line.replace('\n', '').split(delimiter)):
                    data[header] = value
                file_data[row_num] = data
            return file_data

    if headers is False:
        with open(data_file_path, 'r') as text_file:
            text_data = [line.replace('\n', '').split(delimiter)
                         for line in text_file
                         ]
            file_data['headers'] = get_generic_headers(text_data)
            for row_num, row in enumerate(text_data):
                data = OrderedDict()
                for header, value in zip(file_data['headers'], row):
                    data[header] = value
                file_data[row_num] = data
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
                ordered_row = OrderedDict()
                for header in file_data['headers']:
                    ordered_row[header] = row[header]
                file_data[row_num] = ordered_row
            return file_data

    if headers is False:
        with open(data_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            csv_data = list(csv_reader)
            file_data['headers'] = get_generic_headers(csv_data)
            for row_num, row in enumerate(csv_data):
                ordered_row = OrderedDict()
                for header in file_data['header']:
                    ordered_row[header] = row[header]
                file_data[row_num] = ordered_row
            return file_data


def get_delimited_data(data_file_path: str, headers: bool, delimiter):
    """
    Get data from a .tsv file
    :param data_file_path: pathway to file
    :param headers: True if file contains headers, False if file does not contain headers
    :param delimiter: delimiter that separates values in file
    :return: OrderedDict containing the file data
    """
    file_data = OrderedDict()
    if headers is True:
        with open(data_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
            file_data['headers'] = csv_reader.fieldnames
            for row_num, row in enumerate(csv_reader):
                ordered_row = OrderedDict()
                for header in file_data['headers']:
                    ordered_row[header] = row[header]
                file_data[row_num] = ordered_row
            return file_data

    if headers is False:
        with open(data_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            csv_data = list(csv_reader)
            file_data['headers'] = get_generic_headers(csv_data)
            for row_num, row in enumerate(csv_data):
                ordered_row = OrderedDict()
                for header in file_data['header']:
                    ordered_row[header] = row[header]
                file_data[row_num] = ordered_row
            return file_data


def get_json_data(data_file_path: str):
    """
    Get data from a .json file
    :param data_file_path: pathway to file
    :return: OrderedDict containing the file data
    """

    file_data = OrderedDict()
    with open(data_file_path, 'r') as json_file:
        json_data = json.load(json_file, object_pairs_hook=OrderedDict)
        # Get headers
        if type(json_data) == list:
            file_data['headers'] = recursive_json_header(json_data)
            for row_num, row in enumerate(json_data):
                row_data = OrderedDict()
                data = recursive_json_data(row)
                for header, value in zip(file_data['headers'], data):
                    row_data[header] = value
                file_data[row_num] = row_data
            return file_data

        if type(json_data) == OrderedDict:
            json_base_objects = list(json_data.keys())
            for header in json_base_objects:
                current_header = '{}_headers'.format(header)
                file_data[current_header] = recursive_json_header(json_data[header])
                for row_num, row in enumerate(json_data[header]):
                    row_data = OrderedDict()
                    data = recursive_json_data(row)
                    for header, value in zip(file_data[current_header], data):
                        row_data[header] = value
                    file_data['{}_{}'.format(current_header, row_num)] = row_data
            return file_data


def recursive_json_header(json_data, headers=None, header_to_add=None, parent=None):
    """
    Recursive dive into a json object to find the headers of the object
    :param json_data: data to dive into
    :param headers: list of headers found
    :param header_to_add: header to add to the list of headers
    :param parent: parent which may have children
    :return: list of headers for the objects in the json file
    """
    if headers is None:
        headers = list()  # Initialized header list

    # 1st Base Case if you don't have a list or dict you have a sting, int or bool
    if type(json_data) not in (list, OrderedDict) or json_data == []:
        if parent is None:
            headers.append(header_to_add)  # Check to see if there is a base header when appending
        else:
            headers.append(parent + ":" + header_to_add)
            parent = None
        return headers
    # If not base case then you should add the header to base header since we are going deeper into that attribute
    else:
        if parent is None:
            parent = header_to_add
        elif parent is not None and header_to_add:
            parent += ":" + header_to_add
            header_to_add = ""
    # if you have a list check to see if it contains objects
    if type(json_data) == list:
        # If you don't have a list or dict you reached another base case
        if type(json_data[0]) not in (list, OrderedDict):
            if parent is None:
                headers.append(header_to_add)
            else:
                headers.append(parent)
                parent = None
            return headers
        # Your list contains objects
        else:
            recursive_json_header(json_data[0], headers, header_to_add=header_to_add, parent=parent)
    # if you have a dict you know you have a potential header
    if type(json_data) == OrderedDict:
        # find all potential headers in the dict
        possible_headers = json_data.keys()
        # for each item in the dict call method on it's values
        for possible_header in possible_headers:
            if json_data[possible_header] in (OrderedDict, list):
                parent = possible_header
            recursive_json_header(json_data[possible_header], headers,
                                  header_to_add=possible_header, parent=parent)
    return headers


def recursive_json_data(json_data, data=None, parent=None):
    """
    Recursive dive into a json file to find values of the object
    :param json_data: json data to dive into
    :param data: data of the object
    :param parent: parent which may have data
    :return: data for objects in json file
    """
    if data is None:
        data = list()
    # Base case if you don't have a dict or list you have a value
    if type(json_data) not in (list, OrderedDict) or json_data == []:
        data.append(json_data)
        return data
    # 2nd Base case. if you have a list and the first value isn't a list or dict you have a value
    if type(json_data) == list:
        if type(json_data[0]) not in (list, OrderedDict):
            data.append(json_data)
            return data
        else:
            # if you have a list or dict do recursive call on that data
            recursive_json_data(json_data[0], data)
    # if you have a dict you have parents with children that may have values
    if type(json_data) == OrderedDict:
        parents = json_data.keys()
        for parent in parents:
            recursive_json_data(json_data[parent], data, parent)
    return data


def main():
    csv_data = get_csv_data('FL_insurance_sample.csv', headers=True)
    print(csv_data[0].keys())
    print(csv_data['headers'])


if __name__ == '__main__':
    main()
