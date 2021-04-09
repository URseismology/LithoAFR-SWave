# How to use
1. Set the config to make sure those arguments are what you want​
2. Run batch_rover.py​
3. Go to root path of database and run ./launch​

# Data Migration
Use the following code to copy data from BlueHive to Terravibranium
```
rsync -P -avz --delete /scratch/tolugboj_lab/Prj10_DeepLrningEq/9_DanielSequencer/3_src/obspy_batch/ zji@terravibranium.earth.rochester.edu:/RAID6/obspy_data 

```
In Terravibranium, create a linkage between old database root to new one
```
sudo mkdir -p /gpfs/fs2/scratch/tolugboj_lab/Prj10_DeepLrningEq/9_DanielSequencer/3_src/​

sudo chown [user]:[group] /gpfs/fs2/scratch/tolugboj_lab/Prj10_DeepLrningEq/9_DanielSequencer/3_src/​

cd /gpfs/fs2/scratch/tolugboj_lab/Prj10_DeepLrningEq/9_DanielSequencer/3_src/​

ln -s /RAID6/obspy_data obspy_batch
```

# Virtual Environment setup ​
In Terravibranium, you might need to set a Virtual Environment to make sure you have every package you need

1. Create:​
```
python3 -m venv [dir]​
```
​

2. Activate:​
```
source ~/[dir]/bin/activate​
```
​

3. Install all the packages:​
```
Pip3 install ​
```
​
4. Close:​
```
deactivate
```
