import sys
import json

#Observation directory
observation_dir = "../../../../observations/"

#Define workload parameters
workload_type = ["read","write","randread","randwrite"]

queue_depth = [1, 64, 128]

number_of_process = [1, 2, 4, 8]

devices = ["RAM", "SSD"]



def list_all_experiments(node):
    experiments = []
    #TODO: Change the order accordingly!
    for dt in devices:
        for wt in workload_type:
            for qd in queue_depth:
                for np in number_of_process:
                    parameters = {}
                    #parameters["DEVICE"] = devices[dt]
                    parameters["WORKLOAD"] = wt
                    if "read" in wt:
                        parameters["TYPE"] = "read"
                    else:
                        parameters["TYPE"] = "write"
                    parameters["QD"] = qd
                    parameters["NPROCESS"] = np
                    parameters["NAME"] = node+"_"+dt+"_"+wt+"_"+"QD"+str(qd)+"_"+"P"+str(np)
                    experiments.append(parameters)
    
    return experiments


def get_experiment(node, dt, wt, qd, np):
    return node+"_"+dt+"_"+wt+"_"+"QD"+str(qd)+"_"+"P"+str(np)




#Crunch all observations
all_observations = {}
experiments = list_all_experiments('remote_polling')
experiments = ["local_diff_core.json","remote_nice_same_core.json","local_nice_same_core.json","local_same_core.json","local_stonewall.json","remote_diff_core.json","remote_same_core.json","remote_stonewall.json"]
for exp in experiments:
    try:
        with open(observation_dir+exp,'r') as f:
            print(exp)
            data = json.load(f)
            #latency
            obs = data['jobs'][0]["write"]
            obs_dict = {}
            obs_dict['latency'] = obs['clat_ns']
            obs_dict['iops'] = {'min':obs['iops_min'],'max':obs['iops_max'],'mean':obs['iops_mean'],'stddev':obs['iops_stddev'],'N':obs['iops_samples']}
            obs_dict['bw'] = {'min':obs['bw_min'],'max':obs['bw_max'],'mean':obs['bw_mean'],'stddev':obs['bw_dev'],'N':obs['bw_samples']}
            all_observations[exp.split(".")[0]+"_"+"latency"] = obs_dict
            #throughput
            obs = data['jobs'][1]["read"]
            obs_dict = {}
            obs_dict['latency'] = obs['clat_ns']
            obs_dict['iops'] = {'min':obs['iops_min'],'max':obs['iops_max'],'mean':obs['iops_mean'],'stddev':obs['iops_stddev'],'N':obs['iops_samples']}
            obs_dict['bw'] = {'min':obs['bw_min'],'max':obs['bw_max'],'mean':obs['bw_mean'],'stddev':obs['bw_dev'],'N':obs['bw_samples']}
            all_observations[exp.split(".")[0]+"_"+"throughput"] = obs_dict
    except:
        pass



with open('crunched_numbers.json','w') as f:
    json.dump(all_observations, f)
