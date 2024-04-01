sudo modprobe nvme
sudo modprobe nvme-tcp
sudo modprobe nvme-fabrics
sudo nvme connect -t tcp -n nvme-test-target -a $1 -s 4420
