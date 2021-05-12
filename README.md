# Back up of transtomo4Afr code and instructions
the original code for this project can be found on scratch:
/scratch/tolugboj_lab/Prj3_AfricaLithosphere/4_Bin/synthData_bl/jobs_mktestcases_AFR.sh

this is a code that does transdimensional tomography on bluehive using the following scripts
scripts_AFR/mktestcases_AFR.sh
	-- set up the jobs and identify the relevant input datasets.. most important
	AFRANT19_StaLocs: this is file that actually prescribes experiment geometry

scripts_AFR/createsyntheticpaths_AFR.py
	-- output of this file
	sources.dat
	receivers.dat
	paths.dat
	
scripts_AFR/createsyntheticobs_AFR.py
	-- runs the experimental geometry through a synthetic velocity model file:
	-- options including selecting synthetic models, adding noise, 
	-- outputs results to 
	observations.dat
	
scripts_AFR/createsyntheticnamelist.py
	-- sets up the input parameter files in a namelist
	--outputs results to
	input.nml

## Test code... 
--
   
