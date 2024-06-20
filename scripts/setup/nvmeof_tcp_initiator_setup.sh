#provide ip addr and port of target as cmd line arg
sudo modprobe nvme
sudo modprobe nvme-tcp
sudo modprobe nvme-fabrics
sudo nvme connect -t tcp -n nvme-test-target -a $1 -s $2 -P 10 
