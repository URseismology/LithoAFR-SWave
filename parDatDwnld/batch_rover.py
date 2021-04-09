import os
import stat
import pandas as pd
import csv
import configparser


def gen_single_job(root_path, network, station, 
                start, end, src_path, email, manager_file):
    job_name = '{}-{}'.format(network, station)
    job_path = root_path + '/' + network + '/' + job_name
    print(job_path)
    
    if not os.path.exists(job_path):
        os.makedirs(job_path)
    
    run_script_name = job_path + '/job'
    
    with open(run_script_name, 'w') as f:
        f.write('#!/bin/bash\n')
        f.write(f'#SBATCH -o {job_path}/stdout.txt \
                          -e {job_path}/stderr.txt \
                          -J {job_name}\
                          -t 16:00:00 \
                          --mem-per-cpu=1024 \
                          --cpus-per-task 1\n')
        f.write('#SBATCH -A tolugboj_lab -p urseismo\n')
        f.write('module load python3\n')
        #f.write('module load python\n')
        f.write(f'cd {job_path}\n')
        if not os.path.exists(job_path + "/datarepo"):
            f.write('rover init-repository datarepo\n')
        f.write('cd datarepo\n')
        f.write(f'rover retrieve {network}_{station}_*_* {start} {end}\n')
        f.write(f'cd {src_path}\n')
        f.write(f'python3 {src_path}/sum_res.py -n {network} -s {station}\n')
        f.write(f'chgrp -R tolugboj_lab .\n')
        if email:
            f.write(f'{src_path}/email.sh {network} {station} {email}')

    st = os.stat(run_script_name)
    os.chmod(run_script_name, st.st_mode | stat.S_IEXEC)
   
    manager_file.write('cd {} && sbatch job\n'.format(job_path))
    

def gen_manager(db_root_path, network_station_path, src_path,
                start, end, email):
    if not os.path.exists(db_root_path):
        os.makedirs(db_root_path)
    
    manager_script_path = db_root_path + '/launch'
    network_station_list = pd.read_csv(network_station_path)
    
    with open(manager_script_path, 'w') as manager_file:
        manager_file.write('#!/bin/bash\n')
        for index, row in network_station_list.iterrows():
            gen_single_job(db_root_path, row["Network"], row["Station"], start, end, src_path, email, manager_file)

    st = os.stat(manager_script_path)
    os.chmod(manager_script_path, st.st_mode | stat.S_IEXEC)
    
    

if __name__ == "__main__":
    # Parse config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    db_root_path = config.get('path','db_root_path')
    network_station_path = config.get('path','network_station_path')
    src_path = config.get('path','src_path')
    start = config.get('span','start')
    end = config.get('span','end')
    email = config.get('email','email')
    meta_root_path = config.get('path','meta_root_path')
    
    if not os.path.exists(meta_root_path):
        os.makedirs(meta_root_path)
        
    if not os.path.exists(f'{meta_root_path}/download_meta'):
        os.makedirs(f'{meta_root_path}/download_meta')
    
    if not os.path.exists(f'{meta_root_path}/download_sum.csv'):
        with open(f'{meta_root_path}/download_sum.csv', 'w') as csvfile:
            csvfile.write('network,station,location,channel,earliest,latest,updt,intergrity\n')

    gen_manager(db_root_path, network_station_path, src_path,
                start, end, email)
