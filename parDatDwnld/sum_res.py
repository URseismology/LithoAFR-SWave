import os 
import pandas as pd
import numpy as np
import sqlite3 
import glob
import csv
import configparser
import argparse
import subprocess

def intergrity_check(network, station, channel, db_root_path, start, end):
    print(f"cd {db_root_path}/{network}/{network}-{station}/datarepo && rover list-retrieve {network}_{station}_*_{channel} {start} {end}")
    result = subprocess.Popen(f"cd {db_root_path}/{network}/{network}-{station}/datarepo && rover list-retrieve {network}_{station}_*_{channel} {start} {end}", 
                                shell = True, stdout=subprocess.PIPE)
    result.wait()
    (stdout, stderr) = result.communicate()
    intergrity = "Total: 0 N_S_L_C; 0.00 sec" in stdout.decode()
    return intergrity
    
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

    try:
        db_tsindex_sum = pd.read_sql_query("SELECT * FROM tsindex_summary", conn)
        db_tsindex_sum.location = db_tsindex_sum.location.replace("","None",regex = True)
        for index, row in db_tsindex_sum.iterrows():
            channel = row[3]
            db_tsindex_sum.at[index, "intergrity"] = intergrity_check(network, station, channel, db_root_path, start, end)
        
        #print(db_tsindex_sum)
        db_tsindex_sum.to_csv(f'{meta_root_path}/download_sum.csv', mode = "a", sep = ",", index = False, header = False, na_rep = "None")
    except:
        with open(f'{meta_root_path}/sum_fail.txt',"a+") as f:
            f.write(f'{network} {station} \n')

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
