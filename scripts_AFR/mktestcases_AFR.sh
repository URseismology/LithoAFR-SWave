#!/bin/bash

module load urseismo

OUTPUTDIR=../test_cases_09092019
mkdir -p $OUTPUTDIR

if [ -x /usr/bin/python2 ]; 
then
    PYTHON=/usr/bin/python2
else
    PYTHON=python
fi

## number of Processors for individual testing case jobs
numProcs=6

RUNSCRIPT="#!/bin/bash\n\n../../tomo -n input.nml -v\n"
RUNSCRIPT_MPI="#!/bin/bash\n\nmodule load openmpi tomo\n\nmpirun -np ${numProcs} tomo_mpi -n input.nml\n"

#number of individual test
numTest=$1 

##========================================
## This function will create the slurm script 
## file:  job.slurm
## for testing case jobs on urseismo partition 
## on Bluehive
## Usuage:
##   createBHjob $testNum $numProcs $testFolder
## to run the script: sbatch job.slurm
##
##  Baowei Liu <baowei.liu@rochester.edu>
##
##
function createBHjob()
{
  testName=$1
  numProcs=$2
  testFolder=$3 
  jobFile="${testFolder}/job.slurm"

  cat <<EOF > $jobFile 
#!/bin/bash

#SBATCH -J ${testName}
#SBATCH -p urseismo

#SBATCH -t 120:00:00
#SBATCH -n ${numProcs}
#SBATCH -c 1
#SBATCH --mem-per-cpu=8000mb
##SBATCH --nodelist=bhd0048
#SBATCH --mail-type=ALL
#SBATCH --mail-user=urseismobluehivejobs@gmail.com,baowei.liu@rochester.edu

module purge
module load circ slurm
module load openmpi tomo

EOF
#echo 'mpirun -np $SLURM_NTASKS tomo_mpi -n input.nml' >>$jobFile
echo 'mpirun -np $SLURM_NTASKS tomo_mpi -n input.nml --misfit --partitions --hierarchical --voronoi' >>$jobFile
}

#
# Test case 1
# -----------
#
# Longitude    : -10 .. 10
# Latitude     : -10 .. 10
# Sources      : 50
# Receivers    : 50
# Observations : 250
# Tomography   : Uniform 3km/s
#

function test1()
{
  TCDIR=$OUTPUTDIR/tc1
  mkdir -p $TCDIR
  
  MINLON=-20.0
  MAXLON=52.0
  MINLAT=-40.0
  MAXLAT=40.0
  
  echo $MINLON > $TCDIR/bound.txt
  echo $MAXLON >> $TCDIR/bound.txt
  echo $MINLAT >> $TCDIR/bound.txt
  echo $MAXLAT >> $TCDIR/bound.txt
  
  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  #nr=1
  allvalid=`expr $ns \* $nr`
  
  echo $ns "  "  $nr "  "  $allvalid
  
  
  #exit
  #
  $PYTHON createsyntheticpaths_AFR.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -e AFRANT19_StaLocs.txt -f L05_AFRANT19.txt
  #$PYTHON createsyntheticpaths.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat 
#  
  
  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  allvalid=`expr $ns \* $nr`
  
  # half year connection with path range: (40, 500 ) km
  $PYTHON createsyntheticobs_AFR.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -y 0.5 -a 40.0 -b 600.0 -v $allvalid -o $TCDIR/observations.dat -d $TCDIR/data.txt -f L05_AFRANT19.txt -t circularfast4km_AFR -N -n 1.0
#  
  $PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_value 0.1 \
    --vs_std_bd 0.1 \
    --sigma_min 5.0 \
    --sigma_max 20.0 \
    --sigma_std 0.1 \
    --total 1000000 \
    --burnin 0 \
    --thin 100
     
  echo -e $RUNSCRIPT > $TCDIR/run.sh
  echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh
  createBHjob "test1" $numProcs $TCDIR
}  

#
# Test case 2
# -----------
#
# Longitude    : -10 .. 10
# Latitude     : -10 .. 10
# Sources      : 50
# Receivers    : 50
# Observations : 250
# Tomography   : Circular Fast Region in Uniform 3km/s
# Tomography   : Baowei & Tolu
#

function test2()
{
  TCDIR=$OUTPUTDIR/tc2
  mkdir -p $TCDIR
  
  MINLON=-20.0
  MAXLON=52.0
  MINLAT=-40.0
  MAXLAT=40.0
  
  echo $MINLON > $TCDIR/bound.txt
  echo $MAXLON >> $TCDIR/bound.txt
  echo $MINLAT >> $TCDIR/bound.txt
  echo $MAXLAT >> $TCDIR/bound.txt
  
  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  allvalid=`expr $ns \* $nr`
  
  echo $ns "  "  $nr "  "  $allvalid
  
  $PYTHON createsyntheticpaths_AFR.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -e AFRANT19_StaLocs.txt -f L05_AFRANT19.txt
  
  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  allvalid=`expr $ns \* $nr`
  
  $PYTHON createsyntheticobs_AFR.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -y 0.5 -a 40.0 -b 600.0 -v $allvalid -o $TCDIR/observations.dat -d $TCDIR/data.txt -t circularfast4km_AFR -N -n 1.0 --real $TCDIR/observations_real.dat -f L05_AFRANT19.txt
  
  $PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_value 0.1 \
    --vs_std_bd 0.1 \
    --sigma_min 5.0 \
    --sigma_max 20.0 \
    --sigma_std 0.1 \
    --total 1000000 \
    --burnin 0 \
    --thin 100
     
  
  echo -e $RUNSCRIPT > $TCDIR/run.sh
  echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

  createBHjob "test2" $numProcs $TCDIR
}

#
# Test case 3
# -----------
#
# Longitude    : -10 .. 10
# Latitude     : -10 .. 10
# Sources      : 50
# Receivers    : 50
# Observations : 250
# Tomography   : Checkerboard
#
function test3()
{
  TCDIR=$OUTPUTDIR/tc3
  mkdir -p $TCDIR
  
  MINLON=-20.0
  MAXLON=52.0
  MINLAT=-40.0
  MAXLAT=40.0
  
  echo $MINLON > $TCDIR/bound.txt
  echo $MAXLON >> $TCDIR/bound.txt
  echo $MINLAT >> $TCDIR/bound.txt
  echo $MAXLAT >> $TCDIR/bound.txt
  
  $PYTHON createsyntheticpaths_AFR.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -e AFRANT19_StaLocs.txt -f L05_AFRANT19.txt
  
  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  allvalid=`expr $ns \* $nr`
  
  $PYTHON createsyntheticobs_AFR.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -y 0.5 -a 40.0 -b 600.0 -v $allvalid -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard5 -N -n 1.0 -f L05_AFRANT19.txt
  
  $PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_value 0.1 \
    --vs_std_bd 0.1 \
    --sigma_min 5.0 \
    --sigma_max 20.0 \
    --sigma_std 0.1 \
    --total 1000000 \
    --burnin 0 \
    --thin 100
     
  
  echo -e $RUNSCRIPT > $TCDIR/run.sh
  echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

  createBHjob "test3" $numProcs $TCDIR
}

#
# Test case 4
# -----------
#
# Longitude    : -10 .. 10
# Latitude     : -10 .. 10
# Sources      : 200
# Receivers    : 200
# Observations : 4000
# Tomography   : Checkerboard
#

function test4()
{
  TCDIR=$OUTPUTDIR/tc4
  mkdir -p $TCDIR
  
  MINLON=-20.0
  MAXLON=52.0
  MINLAT=-40.0
  MAXLAT=40.0
  
  echo $MINLON > $TCDIR/bound.txt
  echo $MAXLON >> $TCDIR/bound.txt
  echo $MINLAT >> $TCDIR/bound.txt
  echo $MAXLAT >> $TCDIR/bound.txt
  
  $PYTHON createsyntheticpaths_AFR.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 200 -m 200 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -e AFRANT19_StaLocs.txt -f L05_AFRANT19.txt

  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  allvalid=`expr $ns \* $nr`
    
  $PYTHON createsyntheticobs_AFR.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -y 0.5 -a 40.0 -b 600.0 -v $allvalid -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard5 -N -n 1.0 -f L05_AFRANT19.txt
  
  $PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_value 0.1 \
    --vs_std_bd 0.1 \
    --sigma_min 5.0 \
    --sigma_max 20.0 \
    --sigma_std 0.1 \
    --total 1000000 \
    --burnin 0 \
    --thin 100
     
  
  echo -e $RUNSCRIPT > $TCDIR/run.sh
  echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

  createBHjob "test4" $numProcs $TCDIR
}

#
# Test case 5
# -----------
#
# Longitude    : -10 .. 10
# Latitude     : -10 .. 10
# Sources      : 200
# Receivers    : 200
# Observations : 1000
# Tomography   : Checkerboard
# With noise for comparison with TC6
#

function test5()
{
  TCDIR=$OUTPUTDIR/tc5
  mkdir -p $TCDIR
  
  MINLON=-20.0
  MAXLON=52.0
  MINLAT=-40.0
  MAXLAT=40.0
  
  echo $MINLON > $TCDIR/bound.txt
  echo $MAXLON >> $TCDIR/bound.txt
  echo $MINLAT >> $TCDIR/bound.txt
  echo $MAXLAT >> $TCDIR/bound.txt
  
  $PYTHON createsyntheticpaths_AFR.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 200 -m 200 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -e AFRANT19_StaLocs.txt -f L05_AFRANT19.txt

  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  allvalid=`expr $ns \* $nr`
    
  $PYTHON createsyntheticobs_AFR.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -y 0.5 -a 40.0 -b 600.0 -v $allvalid -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard5 -N -n 1.0 -f L05_AFRANT19.txt
  
  $PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_value 0.1 \
    --vs_std_bd 0.1 \
    --sigma_min 5.0 \
    --sigma_max 20.0 \
    --sigma_std 0.1 \
    --total 1000000 \
    --burnin 0 \
    --thin 100
     
  
  echo -e $RUNSCRIPT > $TCDIR/run.sh
  echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

  createBHjob "test5" $numProcs $TCDIR
} #end of test5

# Test case 6
# -----------
#
# Longitude    : -10 .. 10
# Latitude     : -10 .. 10
# Sources      : 200
# Receivers    : 200
# Observations : 1000
# Tomography   : Checkerboard
# Without noise for comparison with TC5
#
function test6()
{
  TCDIR=$OUTPUTDIR/tc6
  mkdir -p $TCDIR
  
  MINLON=-20.0
  MAXLON=52.0
  MINLAT=-40.0
  MAXLAT=40.0
  
  echo $MINLON > $TCDIR/bound.txt
  echo $MAXLON >> $TCDIR/bound.txt
  echo $MINLAT >> $TCDIR/bound.txt
  echo $MAXLAT >> $TCDIR/bound.txt
  
  $PYTHON createsyntheticpaths_AFR.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 200 -m 200 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -e AFRANT19_StaLocs.txt -f L05_AFRANT19.txt

  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  allvalid=`expr $ns \* $nr`
    
  $PYTHON createsyntheticobs_AFR.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -y 0.5 -a 40.0 -b 600.0 -v $allvalid -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard5  -f L05_AFRANT19.txt
  
  $PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_value 0.1 \
    --vs_std_bd 0.1 \
    --sigma_min 5.0 \
    --sigma_max 20.0 \
    --sigma_std 0.1 \
    --total 1000000 \
    --burnin 0 \
    --thin 100
     
    
  
  echo -e $RUNSCRIPT > $TCDIR/run.sh
  echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh
  createBHjob "test6" $numProcs $TCDIR
}

# Test case 7
# -----------
#
# Longitude    : -1 .. 1
# Latitude     : -1 .. 1
# Sources      : 4
# Receivers    : 4
# Observations : 
# Tomography   : Uniform 3km/s
# Without noise for comparison with TC5
#
function test7()
{
  TCDIR=$OUTPUTDIR/tc7
  mkdir -p $TCDIR
  
  MINLON=-20.0
  MAXLON=52.0
  MINLAT=-40.0
  MAXLAT=40.0
  
  echo $MINLON > $TCDIR/bound.txt
  echo $MAXLON >> $TCDIR/bound.txt
  echo $MINLAT >> $TCDIR/bound.txt
  echo $MAXLAT >> $TCDIR/bound.txt
  
  #$PYTHON createfixedpaths.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat 
  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  allvalid=`expr $ns \* $nr`
  
  echo $ns "  "  $nr "  "  $allvalid
  
  $PYTHON createsyntheticpaths_AFR.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -e AFRANT19_StaLocs.txt -f L05_AFRANT19.txt
  
  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  allvalid=`expr $ns \* $nr`
  
  $PYTHON createsyntheticobs_AFR.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -y 0.5 -a 40.0 -b 600.0 -v 900000 -o $TCDIR/observations.dat -d $TCDIR/data.txt -t uniform3km -f L05_AFRANT19.txt
  
  $PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_value 0.1 \
    --vs_std_bd 0.1 \
    --sigma_min 5.0 \
    --sigma_max 20.0 \
    --sigma_std 0.1 \
    --total 1000000 \
    --burnin 0 \
    --thin 100
     
    
  
  echo -e $RUNSCRIPT > $TCDIR/run.sh
  echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

  createBHjob "test7" $numProcs $TCDIR
} #end of test7

#
# Test case 8
# -----------
#
# Longitude    : -10 .. 10
# Latitude     : -10 .. 10
# Sources      : 50
# Receivers    : 50
# Observations : 250
# Tomography   : Checkerboard
# long wave
function test8()
{
  TCDIR=$OUTPUTDIR/tc8
  mkdir -p $TCDIR
  
  MINLON=-20.0
  MAXLON=52.0
  MINLAT=-40.0
  MAXLAT=40.0
  
  echo $MINLON > $TCDIR/bound.txt
  echo $MAXLON >> $TCDIR/bound.txt
  echo $MINLAT >> $TCDIR/bound.txt
  echo $MAXLAT >> $TCDIR/bound.txt
  
  $PYTHON createsyntheticpaths_AFR.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -e AFRANT19_StaLocs.txt -f L05_AFRANT19.txt
  
  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  allvalid=`expr $ns \* $nr`
  
  $PYTHON createsyntheticobs_AFR.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -y 0.5 -a 40.0 -b 4500.0 -v $allvalid -o $TCDIR/observations.dat -d $TCDIR/data.txt -t checkerboard5 -N -n 1.0 -f L05_AFRANT19.txt
  
  $PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_value 0.1 \
    --vs_std_bd 0.1 \
    --sigma_min 5.0 \
    --sigma_max 20.0 \
    --sigma_std 0.1 \
    --total 1000000 \
    --burnin 0 \
    --thin 100
     
  
  echo -e $RUNSCRIPT > $TCDIR/run.sh
  echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

  createBHjob "test8" $numProcs $TCDIR
}

#
# Test case 9
# -----------
#
# Longitude    : -10 .. 10
# Latitude     : -10 .. 10
# Sources      : 50
# Receivers    : 50
# Observations : 250
# Tomography   : Circular Fast Region in Uniform 3km/s
# Tomography   : Baowei & Tolu
#

function test9()
{
  TCDIR=$OUTPUTDIR/tc9
  mkdir -p $TCDIR
  
  MINLON=-20.0
  MAXLON=52.0
  MINLAT=-40.0
  MAXLAT=40.0
  
  echo $MINLON > $TCDIR/bound.txt
  echo $MAXLON >> $TCDIR/bound.txt
  echo $MINLAT >> $TCDIR/bound.txt
  echo $MAXLAT >> $TCDIR/bound.txt
  
  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  allvalid=`expr $ns \* $nr`
  
  echo $ns "  "  $nr "  "  $allvalid
  
  $PYTHON createsyntheticpaths_AFR.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -e AFRANT19_StaLocs.txt -f L05_AFRANT19.txt
  
  ns=`wc -l $TCDIR/sources.dat | awk '{print $1}' `
  nr=`wc -l $TCDIR/receivers.dat | awk '{print $1}' `
  allvalid=`expr $ns \* $nr`
  
  $PYTHON createsyntheticobs_AFR.py -s $TCDIR/sources.dat -r $TCDIR/receivers.dat -p $TCDIR/paths.dat -y 0.5 -a 40.0 -b 4500.0 -v $allvalid -o $TCDIR/observations.dat -d $TCDIR/data.txt -t circularfast4km_AFR -N -n 1.0 --real $TCDIR/observations_real.dat -f L05_AFRANT19.txt
  
  $PYTHON createsyntheticnamelist.py -n $TCDIR/input.nml \
    --vs_std_value 0.1 \
    --vs_std_bd 0.1 \
    --sigma_min 5.0 \
    --sigma_max 20.0 \
    --sigma_std 0.1 \
    --total 1000000 \
    --burnin 0 \
    --thin 100
     
  
  echo -e $RUNSCRIPT > $TCDIR/run.sh
  echo -e $RUNSCRIPT_MPI > $TCDIR/run_mpi.sh

  createBHjob "test9" $numProcs $TCDIR
}

#
# Test 
# -----------
case $numTest in 
  1) test1
     ;;
  2) test2
     ;;
  3) test3
     ;;
  4) test4
     ;;
  5) test5
     ;;
  6) test6
     ;;
  7) test7
     ;;
  8) test8
     ;;
  9) test9
     ;;
  *) echo "only 9 tests available!!!" 
     ;;
esac

