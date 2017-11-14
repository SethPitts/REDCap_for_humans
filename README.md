# redcap_for_humans
Wrapper around some basic REDCap api functions using a command line interface

# Basic Examples

```

$ redcap -create_project my_project
> What is the project redcap url? https://redcapdemo.vanderbilt.edu/
> what is your api token for the project? ****************
New project created at redcap_projects/my_project

$ redcap -project my_project -download records -format  csv
Download complete. Pulled N records saved at my_project/record_downloads/records.csv

$ redcap -p my_project -d records -f json
Donwload complete. Pulled N records saved at my_project/records/download.json

$ redcap -p my_project -d report -id 0001 -f tsv
Report donwload complete. Saved at my_project/report_downloads/report_0001/report_0001.tsv
```