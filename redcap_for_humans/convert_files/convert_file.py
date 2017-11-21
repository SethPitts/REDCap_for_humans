import csv
import json
import sqlite3
from collections import OrderedDict


from redcap_for_humans import convert_files


def convert_to_csv(outfile_path: str, headers: list, data: list):
    """
    Convert the given headers and data to a csv file
    :param outfile_path: pathway to save csv file
    :param headers: headers for csv file
    :param data: data for csv file
    :return: no return
    """
    with open(outfile_path, 'w') as outfile:
        csv_writer = csv.DictWriter(outfile, fieldnames=headers)
        csv_writer.writeheader()
        for row in data:
            csv_writer.writerow(row)

    print('Finished converting to csv. File saved at {}'.format(outfile_path))


def convert_to_delimited_file(outfile_path: str, headers: list, data: list, delimiter: str):
    """
    Convert given headers and data to a file where values are separated by given delimiter
    :param outfile_path: pathway to save file
    :param headers: headers for file
    :param data: data for file
    :param delimiter: delimiter to separate values
    :return: No return.
    """
    with open(outfile_path, 'w') as outfile:
        csv_writer = csv.DictWriter(outfile, fieldnames=headers, delimiter=delimiter)
        csv_writer.writeheader()
        for row in data:
            csv_writer.writerow(row)

    print('Finished converting file. Delimiter is {}. File saved at {}'.format(delimiter, outfile_path))


def convert_to_json(outfile_path:str, data:list):
    """
    Convert given data to json file
    :param outfile_path: pathway to save file
    :param data: data to convert
    :return: No return
    """
    with open(outfile_path, 'w') as outfile:
        json.dump(data, outfile)

    print('Finished converting to json. File saved at {}'.format(outfile_path))


def convert_to_sql_table(database_pathway: str, table_title: str, table_fields: list, table_data: list, drop_table: bool):
    """
    Converts file with given title , headers and data to a sqlite3 table
    :param database_pathway: pathway to database to save table to
    :param table_title: title of table
    :param table_fields: fields for tables, which are headers of the file
    :param table_data: rows of table which are rows in file
    :param drop_table: if True will drop table before attempting to create the table
    :return: No return
    """
    conn = sqlite3.connect(database_pathway)
    cur = conn.cursor()

    table_fields = ",".join(table_fields)
    if drop_table is True:
        drop_table_sql = """DROP TABLE IF EXISTS {}""".format(table_title)
        cur.execute(drop_table_sql)

    # Create Table
    create_table_sql = """CREATE TABLE {} ({})""".format(
        table_title, table_fields)
    print("Creating table {}".format(table_title))
    cur.execute(create_table_sql)

    # Insert Values Statement
    for table_row in table_data:
        transform = "'{}'"
        data_as_text = ",".join(
            [transform.format(item.replace("'", "").replace(",", "")) for item in table_row])
        insert_sql = """INSERT INTO {} VALUES ({})""".format(
            table_title, data_as_text)
        cur.execute(insert_sql)

    # Commit the changes
    conn.commit()
    print("Done Creating table {} in database {}".format(table_title, database_pathway))


def main():
    json_data = convert_files.get_data_from_file.get_json_data('test3.json')
    json_data = iter(json_data.values())
    headers = next(json_data)
    data = [row for row in json_data]
    convert_to_delimited_file('json_to_tsv.tsv', headers, data, delimiter='\t')

    txt_data = convert_files.get_data_from_file.get_text_data('FL_insurance_sample.txt', headers=True, delimiter=',')
    txt_data = iter(txt_data.values())
    headers = next(txt_data)
    data = [row for row in txt_data]
    convert_to_delimited_file('txt_to_tsv.tsv', headers, data, delimiter='\t')

    csv_data = convert_files.get_data_from_file.get_csv_data('FL_insurance_sample.csv', headers=True)
    csv_data = iter(csv_data.values())
    headers = next(csv_data)
    data = [row for row in csv_data]
    convert_to_delimited_file('csv_to_tsv.tsv', headers, data, delimiter='\t')

    txt_data = convert_files.get_data_from_file.get_text_data('FL_insurance_sample.txt', headers=True, delimiter=',')
    txt_data.pop('headers')
    txt_data = [txt_data[key] for key in txt_data.keys()]
    convert_to_json('txt_to_json.json', txt_data)

    csv_data = convert_files.get_data_from_file.get_csv_data('FL_insurance_sample.csv', headers=True)
    csv_data.pop('headers')
    csv_data = [csv_data[key] for key in csv_data.keys()]
    convert_to_json('csv_to_json.json', csv_data)

    tsv_data = convert_files.get_data_from_file.get_delimited_data('nasa_19950801.tsv', headers=True, delimiter='\t')
    print('tsv headers', tsv_data.pop('headers'))
    print(tsv_data[0])
    tsv_data = [tsv_data[key] for key in tsv_data.keys()]
    convert_to_json('tsv_to_json.json', tsv_data)

    csv_data_pathway = 'FL_insurance_sample.csv'
    csv_data = convert_files.get_data_from_file.get_csv_data( csv_data_pathway, headers=True)
    csv_table_title = csv_data_pathway.replace('.csv', '')
    csv_data = iter(csv_data.values())
    csv_table_fields = next(csv_data)
    print("fields are", csv_table_fields)
    csv_table_data = [row.values() for row in csv_data]
    print(csv_table_data)
    convert_to_sql_table('test.db', csv_table_title, csv_table_fields , csv_table_data, drop_table=True)



if __name__ == '__main__':
    main()