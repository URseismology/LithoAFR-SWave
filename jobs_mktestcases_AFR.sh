#!/bin/bash

## to run 8 tests parallely using  mktestcases_AFR.sh 
##

for ((i=1; i<=8; i++))
do
  cat <<EOF > job${i}.slurm
#!/bin/bash
#SBATCH -t 120:00:00
#SBATCH -N 1
#SBATCH -n 1
##SBATCH --mem-per-cpu=750000mb
#SBATCH --nodelist=bhd0048
#SBATCH -J mktest${i} 
#SBATCH -p urseismo
#SBATCH --mail-type=ALL
#SBATCH --mail-user=urseismobluehivejobs@gmail.com

module load urseismo
source activate urseismo

cd /scratch/tolugboj_lab/Prj3_AfricaLithosphere/4_Bin/synthData_bl/scripts_AFR/
srun ./mktestcases_AFR.sh ${i}

EOF
sbatch job${i}.slurm
done
