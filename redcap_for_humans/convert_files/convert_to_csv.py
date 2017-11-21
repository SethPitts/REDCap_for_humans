import csv
import json

from redcap_for_humans import convert_files


def convert_to_csv(out_file_path, headers, data):
    with open(out_file_path, 'w') as outfile:
        csv_writer = csv.DictWriter(outfile, fieldnames=headers)
        csv_writer.writeheader()
        for row in data:
            csv_writer.writerow(row)

    print('Finished converting to csv. File saved at {}'.format(out_file_path))


def convert_to_tsv(out_file_path, headers, data):
    with open(out_file_path, 'w') as outfile:
        csv_writer = csv.DictWriter(outfile, fieldnames=headers, delimiter='\t')
        csv_writer.writeheader()
        for row in data:
            csv_writer.writerow(row)

    print('Finished converting to tsv. File saved at {}'.format(out_file_path))


def main():
    json_data = convert_files.get_data_from_file.get_json_data('test3.json')
    json_data = iter(json_data.values())
    headers = next(json_data)
    data = [row for row in json_data]
    convert_to_tsv('json_to_tsv.tsv', headers, data)

    txt_data = convert_files.get_data_from_file.get_text_data('FL_insurance_sample.txt', headers=True, delimiter=',')
    txt_data = iter(txt_data.values())
    headers = next(txt_data)
    data = [row for row in txt_data]
    convert_to_tsv('txt_to_tsv.tsv', headers, data)

    csv_data = convert_files.get_data_from_file.get_csv_data('FL_insurance_sample.csv', headers=True)
    csv_data = iter(csv_data.values())
    headers = next(csv_data)
    data = [row for row in csv_data]
    convert_to_tsv('csv_to_tsv.tsv', headers, data)


if __name__ == '__main__':
    main()