#!/bin/bash

OUTPUTDIR=../iceland
mkdir -p $OUTPUTDIR

if [ -x /usr/bin/python2 ]; 
then
    PYTHON=/usr/bin/python2
else
    PYTHON=python
fi

RUNSCRIPT="#!/bin/bash\n\n../../tomo -n input.nml -v\n"
RUNSCRIPT_MPI="#!/bin/bash\n\nmpirun -np 4 ../../tomo_mpi -n input.nml\n"

MINLON=-24.0
MAXLON=-12.0
MINLAT=61.0
MAXLAT=67.0

VS_STD_BD=0.0
VS_STD_VALUE=0.025
PD=0.03

SIGMA_MIN=0.1
SIGMA_MAX=5.0
SIGMA_STD=0.05

BURNIN=500000
TOTAL=1000000

#
# Test case 1
# -----------
#
# Longitude    : -10 .. 10
# Latitude     : -10 .. 10
# Sources      : 50
# Receivers    : 50
# Observations : 250
# Tomography   : Checkerboard 5
#

TCDIR=$OUTPUTDIR/tc1
mkdir -p $TCDIR


echo $MINLON > $TCDIR/bound.txt
echo $MAXLON >> $TCDIR/bound.txt
echo $MINLAT >> $TCDIR/bound.txt
echo $MAXLAT >> $TCDIR/bound.txt

$PYTHON createsyntheticpaths.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat 

$PYTHON createsyntheticobs.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -v 250 -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard5 -N -n 1.0

$PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_bd $VS_STD_BD \
    --vs_std_value $VS_STD_VALUE \
    --pd $PD \
    --sigma_min $SIGMA_MIN \
    --sigma_max $SIGMA_MAX \
    --sigma_std $SIGMA_STD \
    --burnin $BURNIN \
    --total $TOTAL \
    --minpartitions 1 \
    --maxpartitions 200 \
    --initpartitions 5

echo -e $RUNSCRIPT > $TCDIR/run.sh
echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

#
# Test case 2
# -----------
#
# Longitude    : -10 .. 10
# Latitude     : -10 .. 10
# Sources      : 50
# Receivers    : 50
# Observations : 250
# Tomography   : Checkerboard 2
#

TCDIR=$OUTPUTDIR/tc2
mkdir -p $TCDIR


echo $MINLON > $TCDIR/bound.txt
echo $MAXLON >> $TCDIR/bound.txt
echo $MINLAT >> $TCDIR/bound.txt
echo $MAXLAT >> $TCDIR/bound.txt

$PYTHON createsyntheticpaths.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat 

$PYTHON createsyntheticobs.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -v 250 -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard2 -N -n 1.0

$PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_bd $VS_STD_BD \
    --vs_std_value $VS_STD_VALUE \
    --pd $PD \
    --sigma_min $SIGMA_MIN \
    --sigma_max $SIGMA_MAX \
    --sigma_std $SIGMA_STD \
    --burnin $BURNIN \
    --total $TOTAL \
    --minpartitions 1 \
    --maxpartitions 200 \
    --initpartitions 5

echo -e $RUNSCRIPT > $TCDIR/run.sh
echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

#
# Test case 3
# -----------
#
# Longitude    : -10 .. 10
# Latitude     : -10 .. 10
# Sources      : 50
# Receivers    : 50
# Observations : 250
# Tomography   : Checkerboard 1
#

TCDIR=$OUTPUTDIR/tc3
mkdir -p $TCDIR


echo $MINLON > $TCDIR/bound.txt
echo $MAXLON >> $TCDIR/bound.txt
echo $MINLAT >> $TCDIR/bound.txt
echo $MAXLAT >> $TCDIR/bound.txt

$PYTHON createsyntheticpaths.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat 

$PYTHON createsyntheticobs.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -v 250 -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard1 -N -n 1.0

$PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_bd $VS_STD_BD \
    --vs_std_value $VS_STD_VALUE \
    --pd $PD \
    --sigma_min $SIGMA_MIN \
    --sigma_max $SIGMA_MAX \
    --sigma_std $SIGMA_STD \
    --burnin $BURNIN \
    --total $TOTAL \
    --minpartitions 1 \
    --maxpartitions 200 \
    --initpartitions 5

echo -e $RUNSCRIPT > $TCDIR/run.sh
echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh


#
# Test case 4
# -----------
#
# Sources      : 50
# Receivers    : 50
# Observations : 1000
# Tomography   : Checkerboard 5
#

TCDIR=$OUTPUTDIR/tc4
mkdir -p $TCDIR


echo $MINLON > $TCDIR/bound.txt
echo $MAXLON >> $TCDIR/bound.txt
echo $MINLAT >> $TCDIR/bound.txt
echo $MAXLAT >> $TCDIR/bound.txt

$PYTHON createsyntheticpaths.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat 

$PYTHON createsyntheticobs.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -v 1000 -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard5 -N -n 1.0

$PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_bd $VS_STD_BD \
    --vs_std_value $VS_STD_VALUE \
    --pd $PD \
    --sigma_min $SIGMA_MIN \
    --sigma_max $SIGMA_MAX \
    --sigma_std $SIGMA_STD \
    --burnin $BURNIN \
    --total $TOTAL \
    --minpartitions 1 \
    --maxpartitions 200 \
    --initpartitions 5

echo -e $RUNSCRIPT > $TCDIR/run.sh
echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

#
# Test case 5
# -----------
#
# Sources      : 50
# Receivers    : 50
# Observations : 1000
# Tomography   : Checkerboard 2
#

TCDIR=$OUTPUTDIR/tc5
mkdir -p $TCDIR


echo $MINLON > $TCDIR/bound.txt
echo $MAXLON >> $TCDIR/bound.txt
echo $MINLAT >> $TCDIR/bound.txt
echo $MAXLAT >> $TCDIR/bound.txt

$PYTHON createsyntheticpaths.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat 

$PYTHON createsyntheticobs.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -v 1000 -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard2 -N -n 1.0

$PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_bd $VS_STD_BD \
    --vs_std_value $VS_STD_VALUE \
    --pd $PD \
    --sigma_min $SIGMA_MIN \
    --sigma_max $SIGMA_MAX \
    --sigma_std $SIGMA_STD \
    --burnin $BURNIN \
    --total $TOTAL \
    --minpartitions 1 \
    --maxpartitions 200 \
    --initpartitions 5

echo -e $RUNSCRIPT > $TCDIR/run.sh
echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

#
# Test case 6
# -----------
#
# Sources      : 50
# Receivers    : 50
# Observations : 1000
# Tomography   : Checkerboard 1
#

TCDIR=$OUTPUTDIR/tc6
mkdir -p $TCDIR


echo $MINLON > $TCDIR/bound.txt
echo $MAXLON >> $TCDIR/bound.txt
echo $MINLAT >> $TCDIR/bound.txt
echo $MAXLAT >> $TCDIR/bound.txt

$PYTHON createsyntheticpaths.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat 

$PYTHON createsyntheticobs.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -v 1000 -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard1 -N -n 1.0

$PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_bd $VS_STD_BD \
    --vs_std_value $VS_STD_VALUE \
    --pd $PD \
    --sigma_min $SIGMA_MIN \
    --sigma_max $SIGMA_MAX \
    --sigma_std $SIGMA_STD \
    --burnin $BURNIN \
    --total $TOTAL \
    --minpartitions 1 \
    --maxpartitions 200 \
    --initpartitions 5

echo -e $RUNSCRIPT > $TCDIR/run.sh
echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

#
# Test case 7
# -----------
#
# Sources      : 50
# Receivers    : 50
# Observations : 2000
# Tomography   : Checkerboard 5
#

TCDIR=$OUTPUTDIR/tc7
mkdir -p $TCDIR


echo $MINLON > $TCDIR/bound.txt
echo $MAXLON >> $TCDIR/bound.txt
echo $MINLAT >> $TCDIR/bound.txt
echo $MAXLAT >> $TCDIR/bound.txt

$PYTHON createsyntheticpaths.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 100 -m 100 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat 

$PYTHON createsyntheticobs.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -v 2000 -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard5 -N -n 1.0

$PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_bd $VS_STD_BD \
    --vs_std_value $VS_STD_VALUE \
    --pd $PD \
    --sigma_min $SIGMA_MIN \
    --sigma_max $SIGMA_MAX \
    --sigma_std $SIGMA_STD \
    --burnin $BURNIN \
    --total $TOTAL \
    --minpartitions 1 \
    --maxpartitions 200 \
    --initpartitions 5

echo -e $RUNSCRIPT > $TCDIR/run.sh
echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

#
# Test case 8
# -----------
#
# Sources      : 50
# Receivers    : 50
# Observations : 2000
# Tomography   : Checkerboard 2
#

TCDIR=$OUTPUTDIR/tc8
mkdir -p $TCDIR


echo $MINLON > $TCDIR/bound.txt
echo $MAXLON >> $TCDIR/bound.txt
echo $MINLAT >> $TCDIR/bound.txt
echo $MAXLAT >> $TCDIR/bound.txt

$PYTHON createsyntheticpaths.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 100 -m 100 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat 

$PYTHON createsyntheticobs.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -v 2000 -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard2 -N -n 1.0

$PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_bd $VS_STD_BD \
    --vs_std_value $VS_STD_VALUE \
    --pd $PD \
    --sigma_min $SIGMA_MIN \
    --sigma_max $SIGMA_MAX \
    --sigma_std $SIGMA_STD \
    --burnin $BURNIN \
    --total $TOTAL \
    --minpartitions 1 \
    --maxpartitions 200 \
    --initpartitions 5

echo -e $RUNSCRIPT > $TCDIR/run.sh
echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

#
# Test case 9
# -----------
#
# Sources      : 50
# Receivers    : 50
# Observations : 2000
# Tomography   : Checkerboard 1
#

TCDIR=$OUTPUTDIR/tc9
mkdir -p $TCDIR


echo $MINLON > $TCDIR/bound.txt
echo $MAXLON >> $TCDIR/bound.txt
echo $MINLAT >> $TCDIR/bound.txt
echo $MAXLAT >> $TCDIR/bound.txt

$PYTHON createsyntheticpaths.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 100 -m 100 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat 

$PYTHON createsyntheticobs.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -v 2000 -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard1 -N -n 1.0

$PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_bd $VS_STD_BD \
    --vs_std_value $VS_STD_VALUE \
    --pd $PD \
    --sigma_min $SIGMA_MIN \
    --sigma_max $SIGMA_MAX \
    --sigma_std $SIGMA_STD \
    --burnin $BURNIN \
    --total $TOTAL \
    --minpartitions 1 \
    --maxpartitions 200 \
    --initpartitions 5

echo -e $RUNSCRIPT > $TCDIR/run.sh
echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh
