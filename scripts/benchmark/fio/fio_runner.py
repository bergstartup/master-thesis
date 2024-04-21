import os
import sys
import subprocess
observation_dir="../../../observations/"
node = sys.argv[1] #Either local or remote

#Define all parameters for the test
devices = {}
devices["RAM"] = "/dev/nvme"
devices["SSD"] = "/dev/nvme"

workload_type = ["read","write","randread","randwrite"]

queue_depth = [1, 64, 128]

number_of_process = [1, 2, 4, 8]


def list_all_experiments():
    experiments = []
    #TODO: Change the order accordingly!
    for dt in devices.keys():
        for wt in workload_type:
            for qd in queue_depth:
                for np in number_of_process:
                    parameters = {}
                    parameters["DEVICE"] = devices[dt]
                    parameters["WORKLOAD"] = wt
                    parameters["QD"] = qd
                    parameters["NPROCESS"] = np
                    parameters["NAME"] = node+"_"+dt+"_"+wt+"_"+"QD"+str(qd)+"_"+"P"+str(np)
                    experiments.append(parameters)
    return experiments

def set_experiment_parameters(parameters):
    for key in parameters.keys():
        os.environ[key] = parameters[key]


def run_fio(fio, op):
    print("Executing ",fio)
    with open(op, 'w') as File:
        subprocess.run("fio "+fio, shell=True, text=True, stdout=File)


def erase_and_pre_condition(device):
    subprocess.run("nvme erase "+device, shell=True, text=False)
    run_fio("pre_condition.fio", "/dev/null")



#**************Main***********************
all_experiments = list_all_experiments()
count_experiment = 0
total_experiments = len(all_experiments)
print("Total number of experiments : ", total_experiments)
for experiment_parameters in all_experiments:
    count_experiment += 1
    print("***************************************************")
    print("Experiment({}/{}):".format(count_experiment, total_experiments),experiment_parameters["NAME"])
    continue
    
    #Execute pre-condition
    erase_and_pre_condition("dev")
    
    #Get output file name
    output_file_name = experiment_parameters["NAME"]
    op = observation_dir + output_file_name
    
    #Set the environemnt variables for the experiment
    set_experiment_parameters(experiment_parameters)
    while True:
        #Run the fio
        run_fio("workload.fio", op)
        break
        #Parse the output to get latency, IOPS, bandwidth and percentile distribution
        #Check the statistical validity with confirm tool
    
