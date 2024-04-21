#Arguments
#!/bin/bash

if [ "-h" == "$1" ]; then
	echo "Requires 4 cmd line args: count device(/dev/nvme?n?) ip port"	
	exit 1
fi

sudo modprobe nvmet
sudo modprobe nvmet-tcp
cd /sys/kernel/config/nvmet/subsystems
sudo mkdir nvme-test-target
cd nvme-test-target/
echo 1 | sudo tee -a attr_allow_any_host > /dev/null
sudo mkdir namespaces/$1
cd namespaces/$1

echo -n $2 |sudo tee -a device_path > /dev/null
echo 1|sudo tee -a enable > /dev/null
sudo mkdir /sys/kernel/config/nvmet/ports/$1
cd /sys/kernel/config/nvmet/ports/$1
echo $3 |sudo tee -a addr_traddr > /dev/null
echo tcp|sudo tee -a addr_trtype > /dev/null
echo $4|sudo tee -a addr_trsvcid > /dev/null
echo ipv4 |sudo tee -a addr_adrfam > /dev/null
sudo ln -s /sys/kernel/config/nvmet/subsystems/nvme-test-target/ /sys/kernel/config/nvmet/ports/$1/subsystems/nvme-test-target
dmesg | grep $3
