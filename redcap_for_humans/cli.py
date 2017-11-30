import argparse
import sys
from collections import OrderedDict

from redcap_for_humans.convert_files import convert_file, get_data_from_file

parser = argparse.ArgumentParser(prog='Redcap for Humans',
                                 description='command line interface to perform some basic redcap api calls')

parser.add_argument('-create_project', help='Create a new redcap project', action='store_true')
parser.add_argument('-download', help='Download the report with the given id')
parser.add_argument('-format', help='format to output file', default='csv')
parser.add_argument('-convert_file', help='Convert file to given file type')
parser.add_argument('-delimiter', help='Delimiter to use when converting to delimited file')


# redcap_for_humans -create_project
# redcap_for_humans -report 1234 -file_type csv
# redcap_for_humans -records -file_type csv


def start():
    file_types = {'.csv': 'csv',
                  '.tsv': 'tsv',
                  '.txt': 'txt',
                  '.json': 'json',
                  }

    def get_file_type(filename):
        for file_type in file_types:
            if filename.endswith(file_type):
                return file_types[file_type]

        print("Could not determine file type")
        sys.exit(1)

    args = parser.parse_args()

    if args.create_project is True:
        pass

    if args.download is not None:
        if args.download not in ('report', 'records'):  # bad entry
            print('please provide the correct arguments')
            sys.exit(1)

        if args.download == 'report':
            pass

        if args.download == 'records':
            pass

    if args.convert_file is not None:
        # get method to pull data from file based on its current type
        file_data_collectors = {'csv': get_data_from_file.get_csv_data,
                                'tsv': get_data_from_file.get_delimited_data,
                                'txt': get_data_from_file.get_text_data,
                                'json': get_data_from_file.get_json_data,
                                }

        # get method to convert file based on the given format will default to csv
        file_converters = {'csv': convert_file.convert_to_csv,
                           'tsv': convert_file.convert_to_delimited_file,
                           'json': convert_file.convert_to_json,
                           'sql': convert_file.convert_to_sql_table,
                           'delimited': convert_file.convert_to_delimited_file,
                           }

        file_pathway = args.convert_file
        current_file_type = get_file_type(file_pathway)

        # get data from the file based on it's file type
        if file_data_collectors.get(current_file_type) is not None:
            collector = file_data_collectors[current_file_type]
            if current_file_type == 'tsv':
                current_file_data = collector(data_file_path=file_pathway, delimiter='\t')
            elif current_file_type == 'json':
                current_file_data = collector(data_file_path=file_pathway)
            else:
                current_file_data = collector(data_file_path=file_pathway, headers=True)
            # get head3ers and data
            current_file_headers_and_data = current_file_data.keys()
            current_file_headers = [current_file_data[header]
                                    for header in current_file_headers_and_data
                                    if header.find('headers')
                                    ]
            current_file_data_to_write = [current_file_data[data_key]
                                          for data_key in current_file_headers_and_data
                                          if not data_key.find('headers')
                                          ]
        else:
            print('can not parse curren file type')
            sys.exit(1)

        # convert file to the requested format
        format_to_convert = args.format
        if file_converters.get(format_to_convert) is not None:
            converter = file_converters.get(format_to_convert)
            new_file_name = file_pathway.replace(current_file_type, format_to_convert)
            # TODO: deal with duplicate files by adding a number to the end?

            if format_to_convert == 'tsv':
                converter(outfile_path=new_file_name, headers=current_file_headers, data=current_file_data_to_write,
                          delimiter='\t')
            if format_to_convert == 'delimited':
                if args.delimiter is not None:
                    converter(outfile_path=new_file_name, headers=current_file_headers, data=current_file_data_to_write,
                              delimiter=args.delimiter)
                else:
                    print('please provide a delimiter')
                    sys.exit(1)
            if format_to_convert == 'csv':
                converter(outfile_path=new_file_name, headers=current_file_headers, data=current_file_data_to_write)
            if format_to_convert == 'json':
                pass # damn you json
            if format_to_convert == 'sql':
                table_title = new_file_name.replace(format_to_convert + ".", "")
                converter(outfile_path=new_file_name, table_title=table_title, table_fields=current_file_headers,
                          table_data=current_file_data_to_write, drop_table=True)
