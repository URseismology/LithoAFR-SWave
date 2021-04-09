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
    #print(f"cd {db_root_path}/{network}/{network}-{station}/datarepo && rover list-retrieve {network}_{station}_*_{channel} {start} {end}")
    result = subprocess.Popen(f"cd {db_root_path}/{network}/{network}-{station}/datarepo && rover list-retrieve {network}_{station}_*_{channel} {start} {end}", 
                                shell = True, stdout=subprocess.PIPE)
    result.wait()
    (stdout, stderr) = result.communicate()
    intergrity = "Total: 0 N_S_L_C; 0.00 sec" in stdout.decode()
    return intergrity

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

sum_db = sqlite3.connect(f"{meta_root_path}/sum.db")
sum_cur = sum_db.cursor()
sum_cur.execute("""
    create table if not exists "summary"(
    network text,
    station text,
    location text,
    channel text,
    earliest text,
    latest text,
    updt text,
    integrity text,
    primary key(network, station, channel));
    """)

for db_path in glob.glob(f"{db_root_path}/*/*/datarepo/data/timeseries.sqlite"):
    print(db_path)
    station_db = sqlite3.connect(db_path)
    station_cur = station_db.cursor()
    
    
    try:
        station_sum = station_cur.execute("SELECT * FROM tsindex_summary;").fetchall()
        #print(station_sum)
        
        #print(db_tsindex_sum)
        #db_tsindex_sum.to_csv(f'{meta_root_path}/download_sum.csv', mode = "a", sep = ",", index = False, header = False, na_rep = "None")
    except:
        with open(f'{meta_root_path}/sum_fail.txt',"a+") as f:
            f.write(f'{network} {station} \n')
    for row in station_sum:
            network, station, location, channel, earliest,latest, updt = row
            integrity = intergrity_check(network, station, channel, db_root_path, start, end)
            #print(network, station, location, channel, earliest,latest, updt, integrity)
            if not location:
                location = "NaN"

            sum_cur.execute("""
                replace into summary
                values(?,?,?,?,?,?,?,?);
                """, (network, station, location, channel, earliest,latest, updt, integrity))
            sum_db.commit()
    station_cur.close()
sum_cur.close()
          
    #print(sum_cur.execute("SELECT * FROM summary;").fetchall())
conn = sqlite3.connect(f"{meta_root_path}/sum.db", isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)
download_summary = pd.read_sql_query("SELECT * FROM summary", conn)
download_summary.to_csv(f"{meta_root_path}/download_summary.csv",index=False)
conn.close()

