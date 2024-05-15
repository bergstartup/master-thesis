import os
import time
import sys
import subprocess
import confirm_tool
import signal


observation_dir="../../../observations/performance/"
confidence_level = 0.95
error_bound = 0.05
log_dir = "./logs/"
NCPUS = 8
node = sys.argv[1] #Either local or remote
devices = {}
devices["RAM"] = os.environ("S_DEVICE")
devices["SSD"] = os.environ("P_DEVICE")

#Define workload parameters
workload_type = ["randread","randwrite","read","write"]

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

def run_fio(fio, op, cpus = [i for i in range(NCPUS)]):
    cpu_string = ','.join(map(str, cpus))
    with open(op, 'w') as File:
        subprocess.run("taskset -c {} fio --output-format=json {}".format(cpu_string, fio), shell=True, text=True, stdout=File)


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


def run_tcp_trace(fop):
    p = subprocess.Popen(["bpftrace","../../bpf/tcptrace.bt","-o",fop+"_bpf"])
    time.sleep(5)
    return p

#**************Main***********************
#Execute pre conditioning
for device in devices.keys(): 
    break
    erase_and_pre_condition(devices[device])


print("Running bpf trace to collect keep alive data")
p = run_tcp_trace(observation_dir + "keep_alive_bpf")
time.sleep(10)
p.send_signal(signal.SIGINT)



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
    for iter_count in range(1, 16):
        os.environ["TIME"] = str(120) 

        #run tcp_trace
        #p = run_tcp_trace(op)
        #Run the fio
        print("{}) Executing experiment".format(iter_count))
        run_fio("workload.fio", op, [i for i in range(experiment_parameters["NPROCESS"])])
        #kill tcp_trace
        #p.send_signal(signal.SIGINT)

        #Parse the output to get latency, IOPS, bandwidth and percentile distribution 
        #Check the statistical validity with confirm tool
        if statisticaly_valid(experiment_parameters["NAME"], iter_count * 5):
            break
        print("Not valid")
