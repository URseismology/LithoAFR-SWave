import os 
import pandas as pd
import numpy as np
import sqlite3 
import glob
import csv
import configparser
import argparse
import subprocess

"""
Extract the meta data from a specific station by reading its timeseries.sqlite
"""
def gen_meta_data(network, station, db_root_path, meta_root_path, start, end):

    if not os.path.exists(meta_root_path):
        os.makedirs(meta_root_path)
        
    db_path = f"{db_root_path}/{network}/{network}-{station}/datarepo/data/timeseries.sqlite"
    #print(db_path)
    conn = sqlite3.connect(db_path, isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)                 
    try: 
        db_tesindex = pd.read_sql_query("SELECT * FROM tsindex", conn)
    except:
        with open(f'{meta_root_path}/tsindex_fail.txt',"a+") as f:
            f.write(f'{network} {station} \n')

    if not os.path.exists(f'{meta_root_path}/download_meta'):
        os.makedirs(f'{meta_root_path}/download_meta')
    db_tesindex.to_csv(f'{meta_root_path}/download_meta/{network}-{station}.csv', index=False)
    subprocess.run(f"chgrp tolugboj_lab {meta_root_path}/download_meta/{network}-{station}.csv", shell=True, check=True)

config = configparser.ConfigParser()
config.read('config.ini')
db_root_path = config.get('path','db_root_path')
meta_root_path = config.get('path','meta_root_path')
start = config.get('span','start')
end = config.get('span','end')

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--station", type = str)
parser.add_argument("-n", "--network", type = str)
args = parser.parse_args()

gen_meta_data(args.network, args.station, db_root_path, meta_root_path, start, end)
