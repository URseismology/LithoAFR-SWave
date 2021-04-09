import os 
import pandas as pd
import numpy as np
import sqlite3 
import glob
import csv
import configparser
import argparse
import subprocess
import time


            
"""
use rover list-retrieve to check whether the database is fully synchronized with IRIS server
"""
def intergrity_check(network, station, channel, db_root_path, start, end):
    #print(f"cd {db_root_path}/{network}/{network}-{station}/datarepo && rover list-retrieve {network}_{station}_*_{channel} {start} {end}")
    # use subprocess to run rover in shell
    result = subprocess.Popen(f"cd {db_root_path}/{network}/{network}-{station}/datarepo && rover list-retrieve {network}_{station}_*_{channel} {start} {end}", 
                                shell = True, stdout=subprocess.PIPE)
    result.wait()
    # get result of the rover, "Total: 0 N_S_L_C; 0.00 sec" means it is completed
    (stdout, stderr) = result.communicate()
    intergrity = "Total: 0 N_S_L_C; 0.00 sec" in stdout.decode()
    return intergrity


"""
Get all args from config
"""
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

"""
Create a sqlite database for download_summary and integrity_summary
Loop the whole database and look for sqlite file
Extract tsindex_summary from sqlite file,
and append it into download_summary
do intergrity check for each station and append result to integrity_summary
"""

sum_db = sqlite3.connect(f"{meta_root_path}/sum.db")
sum_cur = sum_db.cursor()
sum_cur.execute("""
    create table if not exists "download_summary"(
    network text,
    station text,
    location text,
    channel text,
    earliest text,
    latest text,
    updt text,
    primary key(network, station, channel));
    """)
    
sum_cur.execute("""
    create table if not exists "integrity_summary"(
    network text,
    station text,
    integrity text,
    primary key(network, station));
    """)

for db_path in glob.glob(f"{db_root_path}/*/*/datarepo/data/timeseries.sqlite"):
    print(db_path)
    station_db = sqlite3.connect(db_path)
    station_cur = station_db.cursor()
    
    station_sum = []
    try:
        station_sum = station_cur.execute("SELECT * FROM tsindex_summary;").fetchall()
        #print(station_sum)
        
        #print(db_tsindex_sum)
        #db_tsindex_sum.to_csv(f'{meta_root_path}/download_sum.csv', mode = "a", sep = ",", index = False, header = False, na_rep = "None")
    except:
        with open(f'{meta_root_path}/sum_fail.txt',"a+") as f:
            f.write(f'{db_path} \n')
    for row in station_sum:
            network, station, location, channel, earliest,latest, updt = row
            #print(network, station, location, channel, earliest,latest, updt)
            if not location:
                location = "NaN"

            sum_cur.execute("""
                replace into download_summary
                values(?,?,?,?,?,?,?);
                """, (network, station, location, channel, earliest,latest, updt))
    integrity = intergrity_check(network, station, "*", db_root_path, start, end)
    time.sleep(1)
    sum_cur.execute("""
                replace into integrity_summary
                values(?,?,?);
                """, (network, station, integrity))
    sum_db.commit()
    station_cur.close()
sum_cur.close()
          
    #print(sum_cur.execute("SELECT * FROM summary;").fetchall())
conn = sqlite3.connect(f"{meta_root_path}/sum.db", isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)
download_summary = pd.read_sql_query("SELECT * FROM download_summary", conn)
download_summary.to_csv(f"{meta_root_path}/download_summary.csv",index=False)
subprocess.run(f"chgrp tolugboj_lab {meta_root_path}/download_summary.csv", shell=True, check=True)

#integrity_summary = pd.read_sql_query("SELECT * FROM integrity_summary", conn)
#integrity_summary.to_csv(f"{meta_root_path}/integrity_summary.csv",index=False)
#subprocess.run(f"chgrp tolugboj_lab {meta_root_path}/integrity_summary.csv", shell=True, check=True)
conn.close()

