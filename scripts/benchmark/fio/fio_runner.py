import os
import sys
import subprocess
observation_dir="../../../observations/"
fio_workload_dir="./workloads/"

def list_fio_scripts(directory):
    return [entry.name for entry in os.scandir(directory)]

def run_fio(fio, op):
    print("Executing ",fio)
    with open(op, 'w') as File:
        subprocess.run("fio "+fio, shell=True, text=True, stdout=File)


#Execute pre-condition
run_fio("pre_condition.fio", "/dev/null")
workload_type = sys.argv[1] #Either local or remote
fio_scripts = list_fio_scripts(fio_workload_dir)
for script in fio_scripts:
    output_file_name = workload_type + "_" + script.split(".")[0]
    op = observation_dir + output_file_name
    run_fio(script, op)
