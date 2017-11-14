import csv
import requests

"""Example of using request to pull a report. I think we should create a generic api call function
that can be used, but we may have to break it into calls for reports and calls for records but 
this is just an example"""


def get_report(report_id, token, url, outfile):
    """
    Pulls the given report in its labeled form in the csv format
    :param report_id: id of the report to pull
    :param token: users api token
    :param url: url for redcap project
    :param outfile: name to give the downloaded file
    :return: No return
    """

    # API to pull reports
    payload = {'token': token, 'format': 'csv', 'content': 'report',
               'report_id': report_id, 'rawOrLabelHeaders': 'label',
               'rawOrLabel': 'label', 'exportCheckboxLabel': True}

    response = requests.post(url, data=payload, verify=True)
    print(response.status_code)
    # Successful call
    if response.status_code == 200:
        with open(outfile, 'w') as fout:
            output_writer = csv.writer(fout)
            # Get CSV data from the response
            # We encode with the ignore option because because we had some chinese data with
            #  weird unicode characters
            data = csv.reader(response.text.encode('ascii', 'ignore').split("\n"))
            count = 0
            for row in data:
                if not row:  # Can't remember why we had to break here. Comment your code
                    print('Done, pulled {} records'.format(count))
                    break
                output_writer.writerow(row)
                count += 1
    else:
        print("Failed")
        raise RuntimeError


def main():
    with open('token.txt', 'r') as token_file:
        token = next(token_file).strip()
        url = 'https://redcapdemo.vanderbilt.edu'
        outfile = 'pulled_report.csv'
        get_report('0001', token, url, outfile)


if __name__ == "__main__":
    main()
