import os
import sys
import json

obs_dir="../../../observations/network/"
files = os.listdir(obs_dir)

crunched_numbers = {}
for i in files:
    if "crunched" in i:
        continue
    try:
        with open(obs_dir+i,"r") as fp:
            d = json.load(fp)
            bw =  d["end"]["sum_sent"]["bits_per_second"]
            #mbps to GBps
            bw = bw/(8*(1024**3))
            try:
                crunched_numbers[i.split("_")[2]][i.split("_")[1]] = bw
            except:
                crunched_numbers[i.split("_")[2]] = {}
                crunched_numbers[i.split("_")[2]][i.split("_")[1]] = bw
    except Exception as e:
        print(i, e)

with open(obs_dir+"crunched_numbers.json","w") as fp:
    json.dump(crunched_numbers, fp)
