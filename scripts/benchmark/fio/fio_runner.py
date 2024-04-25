import os
import sys
import subprocess
import confirm_tool


observation_dir="../../../observations/"
confidence_level = 0.95
error_bound = 0.05
log_dir = "./logs/"

node = sys.argv[1] #Either local or remote

#Parse available NVMe devices
devices = {}
def parse_and_identify_device_type(nvme_list_op):
    dev_path = nvme_list_op.split()[0]
    if "FEMU" in nvme_list_op:
        print("RAM backed NVMe device : ", dev_path)
        devices["RAM"] = dev_path
    else:
        print("NVMe SSD device: ",dev_path)
        devices["SSD"] = dev_path

print("Identiying SSD devices")
device_list = subprocess.check_output(["nvme", "list"])
devices_str = device_list.decode().split("\n")[2:]
if len(devices_str) == 0:
    print("ABORT: No NVMe devices identified")
    sys.exit(-1)

#Check for RAM backed SSD emulation
parse_and_identify_device_type(devices_str[0])

if len(devices_str) < 2:
    print("WARNING : Only one NVMe device is identified")
else:
    parse_and_identify_device_type(devices_str[1])
print("\n")



#Define workload parameters
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
        os.environ[key] = str(parameters[key])

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

all_experiments = list_all_experiments()
count_experiment = 0
total_experiments = len(all_experiments)
print("Total number of experiments : ", total_experiments)
for experiment_parameters in all_experiments:
    count_experiment += 1
    print("***************************************************")
    print("Experiment({}/{}):".format(count_experiment, total_experiments),experiment_parameters["NAME"])
    
    #Get output file name
    output_file_name = experiment_parameters["NAME"]
    op = observation_dir + output_file_name

    #Set the environemnt variables for the experiment
    set_experiment_parameters(experiment_parameters)
    for iter_count in range(1,16):
        os.environ["TIME"] = str(iter_count * 5)
        #Run the fio
        print("({})Executing experiment".format(iter_count))
        run_fio("workload.fio", op)
        #Parse the output to get latency, IOPS, bandwidth and percentile distribution 
        #Check the statistical validity with confirm tool
        if statisticaly_valid(experiment_parameters["NAME"], iter_count * 5):
            break
        print("Not valid")
    break
