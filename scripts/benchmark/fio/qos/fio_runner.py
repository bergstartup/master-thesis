import os
import time
import sys
import subprocess
#import confirm_tool
import signal


observation_dir="../../../../observations/qos/"
confidence_level = 0.95
error_bound = 0.05
log_dir = "./logs/"

node = sys.argv[1] #Either local or remote
devices = {}
devices["SSD"] = "/dev/nvme0n2"
experiments = ["same_core", "nice_same_core", "nice_prio_same_core", "diff_core", "prio_diff_core", "stonewall"]


def set_experiment_parameters(parameters):
    os.environ["DEVICE"] = devices["SSD"]
    os.environ["LCPU"] = "0"
    os.environ["TCPU"] = "0"
    os.environ["STONEWALL"] = "0" 
    #Set to default NICE and IONICE value
    os.environ["LNICE"] = "0"
    os.environ["TNICE"] = "0"
    os.environ["LPRIO"] = "4"
    os.environ["TPRIO"] = "4"
    if "diff" in parameters:
        os.environ["TCPU"] = "1"
    if "nice" in parameters:
        os.environ["LNICE"] = "-19"
    if "prio" in parameters:
        os.environ["LPRIO"] = "0"
    if "stonewall" in parameters:
        os.environ["STONEWALL"] = "1"

def run_fio(fio, op):
    with open(op, 'w') as File:
        subprocess.run("fio --output-format=json {}".format(fio), shell=True, text=True, stdout=File)


def erase_and_pre_condition(device):
    print("Pre conditioning device : ", device)
    subprocess.run("nvme format "+device, shell=True, text=False)
    #Set the device
    os.environ["DEVICE"] = device
    run_fio("pre_condition.fio", "/dev/null")


def statisticaly_valid(exp_name, entries):
    return True
    parameters = ["clat","bw","iops"]
    for para in parameters:
        file_path = "{}{}_{}.log".format(log_dir, exp_name, para)
        obs = confirm_tool.get_obs_from_log(file_path)
        if len(obs) == 0:
            return False
        #Remove the logs during RAMP time
        obs = obs[10:]
        #Reduce observations
        valid = confirm_tool.apply_confirm(obs, confidence_level, error_bound)
        if not valid:
            return False

    return True


#**************Main***********************
#Execute pre conditioning
for device in devices.keys(): 
    break
    erase_and_pre_condition(devices[device])




count_experiment = 0
total_experiments = len(experiments)
print("Total number of experiments : ", total_experiments)
for experiment_parameters in experiments:
    count_experiment += 1
    print("***************************************************")
    print("Experiment({}/{}):".format(count_experiment, total_experiments),experiment_parameters)
    
    #Get output file name
    output_file_name = node +"_"+experiment_parameters+".json"
    op = observation_dir + output_file_name

    #Set the environemnt variables for the experiment
    set_experiment_parameters(experiment_parameters)
    for iter_count in range(1, 16):
        #Run the fio
        print("{}) Executing experiment".format(iter_count))
        run_fio("lt.fio", op)

        #Parse the output to get latency, IOPS, bandwidth and percentile distribution 
        #Check the statistical validity with confirm tool
        if statisticaly_valid(experiment_parameters, iter_count * 5):
            break
