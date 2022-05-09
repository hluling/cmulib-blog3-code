import pandas as pd
import json
import os
from zipfile import ZipFile
import io
from io import BytesIO, StringIO

# convenience function #1:
# read all non-hidden files
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

# convenience function #2:
# read all non-hidden zip files
def listzipdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.') and f.endswith('.zip'):
            yield f 

cwd = os.path.dirname(os.path.realpath(__file__))

data_dir = os.path.join(cwd, "data")
months = sorted(list(listdir_nohidden(data_dir)))

month_dirs = [os.path.join(data_dir, month) for month in months]

for month_dir in month_dirs:

    for group_zip in sorted(listzipdir_nohidden(month_dir)):
        group_dir = os.path.join(month_dir, group_zip)
        
        '''
        From Line 38 to Line 48:
        Core of reading nested zip files withouting extracting
        '''
        with ZipFile(group_dir) as zf:
            csv_zips = zf.namelist()
            for csv_zip in csv_zips:
                #print(csv_zip)
                with zf.open(csv_zip) as csv_zip_fh:
                    csv_zip_fhdata = BytesIO(csv_zip_fh.read())
                    #print(csv_zip_fhdata)
                    with ZipFile(csv_zip_fhdata) as zcsv:
                        csv_file = zcsv.namelist()[0]
                        with zcsv.open(csv_file, mode='r') as the_csv:
                            df = pd.read_csv(the_csv)
                            print(group_dir, csv_file, len(df))