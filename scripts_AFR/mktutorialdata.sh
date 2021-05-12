#!/bin/bash

OUTPUTDIR=../tutorial
mkdir -p $OUTPUTDIR

if [ -x /usr/bin/python2 ]; 
then
    PYTHON=/usr/bin/python2
else
    PYTHON=python
fi

#
# Longitude    : -10 .. 10
# Latitude     : -10 .. 10
# Sources      : 50
# Receivers    : 50
# Observations : 250
# Tomography   : Gaussian peak centred at 0,0
#

DDIR=$OUTPUTDIR/data
mkdir -p $DDIR

MINLON=-10.0
MAXLON=10.0
MINLAT=-10.0
MAXLAT=10.0

echo $MINLON > $DDIR/bound.txt
echo $MAXLON >> $DDIR/bound.txt
echo $MINLAT >> $DDIR/bound.txt
echo $MAXLAT >> $DDIR/bound.txt

$PYTHON createsyntheticpaths.py --minlon $MINLON --maxlon $MAXLON --minlat $MINLAT --maxlat $MAXLAT -n 50 -m 50 -s $DDIR/sources.dat -r $DDIR/receivers.dat -p $DDIR/paths.dat 

$PYTHON createsyntheticobs.py -s $DDIR/sources.dat -r $DDIR/receivers.dat -p $DDIR/paths.dat -v 250 -o $DDIR/observations.dat -d $DDIR/data.txt -t gaussian2x4 -N

$PYTHON createsyntheticobs.py -s $DDIR/sources.dat -r $DDIR/receivers.dat -p $DDIR/paths.dat -v 1000 -o $DDIR/observations_detailed.dat -d $DDIR/data.txt -t gaussian2x4 -N
