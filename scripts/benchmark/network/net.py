import subprocess

obs_dir = "../../../observations/network/"
BS = ["4","8","16","32","64","128", "256", "512"]
NP = [1, 2, 3, 4, 5, 6, 7, 8]
for i in BS:
    for j in NP:
        with open(obs_dir+"tcpbw_S{}_{}".format(j,i),"w") as f:
            subprocess.run("./tcp_bw.sh {} {}".format(j,i), shell=True, stdout=f)
