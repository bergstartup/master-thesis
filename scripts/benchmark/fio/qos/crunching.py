import sys
import os
import json

#Observation directory
observation_dir = "../../../../observations/qos/"
all_observations = {}
#experiments = ["local_same_stonewall.json","local_nice_stonewall.json","local_nice_diff_core.json","local_prio_diff_core.json","remote_nice_prio_same_core.json","local_nice_prio_same_core.json","local_prio_same_core.json","remote_prio_same_core.json","local_diff_core.json","remote_nice_same_core.json","local_nice_same_core.json","local_same_core.json","local_stonewall.json","remote_diff_core.json","remote_same_core.json","remote_stonewall.json"]
experiments = os.listdir(observation_dir)
for exp in experiments:
    if "crunched_numbers_qos.json" == exp:
        continue
    try:
        with open(observation_dir+exp,'r') as f:
            print(exp)
            data = json.load(f)
            #latency
            obs = data['jobs'][0]["read"]
            obs_dict = {}
            obs_dict['latency'] = obs['clat_ns']
            obs_dict['iops'] = {'min':obs['iops_min'],'max':obs['iops_max'],'mean':obs['iops_mean'],'stddev':obs['iops_stddev'],'N':obs['iops_samples']}
            obs_dict['bw'] = {'min':obs['bw_min'],'max':obs['bw_max'],'mean':obs['bw_mean'],'stddev':obs['bw_dev'],'N':obs['bw_samples']}
            all_observations[exp.split(".")[0]] = obs_dict
            #throughput
            """
            obs = data['jobs'][1]["read"]
            obs_dict = {}
            obs_dict['latency'] = obs['clat_ns']
            obs_dict['iops'] = {'min':obs['iops_min'],'max':obs['iops_max'],'mean':obs['iops_mean'],'stddev':obs['iops_stddev'],'N':obs['iops_samples']}
            obs_dict['bw'] = {'min':obs['bw_min'],'max':obs['bw_max'],'mean':obs['bw_mean'],'stddev':obs['bw_dev'],'N':obs['bw_samples']}
            all_observations[exp.split(".")[0]+"_"+"throughput"] = obs_dict
            """
    except:
        pass



with open(observation_dir+'crunched_numbers_qos.json','w') as f:
    json.dump(all_observations, f)
